# =============================================================================
# JarDiscordEngine - Python Discord Bot Engine (pycord-based)
# =============================================================================
#
# JarDiscordEngine is a lightweight bot framework built on top of pycord
# that simplifies Discord bot development while providing higher-level
# abstractions for command management, event handling, and extensibility.
#
# =============================================================================
# Version: jardiscordengine-v1
# Author: Jarjarbin Studio
# License: GPL v3
# =============================================================================
#
# This engine is inspired by pycord, modern bot framework design patterns,
# and modular software architecture.
#
# It is designed for educational purposes and small-to-medium Discord bot
# projects.
#
# It provides structured systems such as automatic command discovery,
# command registration, event handling, extension management, and shared
# services for logging, configuration, and permissions.
#
# =============================================================================
# WARNING:
# =============================================================================
#
# This is NOT pycord itself.
# It is a custom abstraction layer built on top of pycord.
#
# =============================================================================

_JDE_COMMAND_METADATA = "__jde_command_metadata__"

def _get_metadata(callback):
    if not callable(callback):
        raise TypeError("CALLBACK must be callable")

    metadata = getattr(callback, _JDE_COMMAND_METADATA, None)

    if metadata is None:
        metadata = {
            "is_command": False,
            "name": None,
            "description": None,
            "options": [],
            "permissions": {},
            "bot_permissions": {},
            "guild_only": False,
            "owner_only": False,
            "checks": [],
            "cooldown": None
        }

        setattr(callback, _JDE_COMMAND_METADATA, metadata)

    return metadata

def _validate_text(value, name, maximum):
    if not isinstance(value, str):
        raise TypeError(f"{name.upper()} must be str")

    if not value:
        raise ValueError(f"{name.upper()} cannot be empty")

    if len(value) > maximum:
        raise ValueError(f"{name.upper()} cannot exceed {maximum} characters")

def command(name, description):
    _validate_text(name, "command name", 32)
    _validate_text(description, "command description", 100)

    if not name.islower() or any(
        not (character.isalnum() or character in "-_")
        for character in name
    ):
        raise ValueError("COMMAND NAME must use lowercase letters, numbers, '-' or '_'")

    def decorator(callback):
        metadata = _get_metadata(callback)

        if metadata["is_command"]:
            raise ValueError("Callback is already registered as a command")

        metadata["is_command"] = True
        metadata["name"] = name
        metadata["description"] = description

        return callback

    return decorator

def has_permissions(**permissions):
    if not permissions:
        raise ValueError("At least one permission must be specified")

    if any(not isinstance(value, bool) for value in permissions.values()):
        raise TypeError("Permission values must be bool")

    def decorator(callback):
        metadata = _get_metadata(callback)

        for name, value in permissions.items():
            if name in metadata["permissions"]:
                raise ValueError(f"Permission {name!r} is already configured")

            metadata["permissions"][name] = value

        return callback

    return decorator

def bot_has_permissions(**permissions):
    if not permissions:
        raise ValueError("At least one permission must be specified")

    if any(not isinstance(value, bool) for value in permissions.values()):
        raise TypeError("Permission values must be bool")

    def decorator(callback):
        metadata = _get_metadata(callback)

        for name, value in permissions.items():
            if name in metadata["bot_permissions"]:
                raise ValueError(f"Bot permission {name!r} is already configured")

            metadata["bot_permissions"][name] = value

        return callback

    return decorator

def guild_only():
    def decorator(callback):
        metadata = _get_metadata(callback)
        metadata["guild_only"] = True

        return callback

    return decorator

def is_owner():
    def decorator(callback):
        metadata = _get_metadata(callback)
        metadata["owner_only"] = True

        return callback

    return decorator

def checks(*callbacks):
    if not callbacks:
        raise ValueError("At least one check must be specified")

    if not all(callable(callback) for callback in callbacks):
        raise TypeError("All checks must be callable")

    def decorator(callback):
        metadata = _get_metadata(callback)
        metadata["checks"][0:0] = callbacks

        return callback

    return decorator

def option(name, description, option_type, required = True, choices = None, min_value = None, max_value =  None, min_length = None, max_length = None):
    _validate_text(name, "option name", 32)
    _validate_text(description, "option description", 100)

    if not isinstance(required, bool):
        raise TypeError("REQUIRED must be bool")

    supported_types = (
        str, int, float, bool,
        "user", "channel", "role", "mentionable", "attachment"
    )

    if option_type not in supported_types:
        raise TypeError("Unsupported option type")

    if choices is not None and not isinstance(choices, (list, tuple)):
        raise TypeError("CHOICES must be a list or tuple")

    def decorator(callback):
        metadata = _get_metadata(callback)

        if any(item["name"] == name for item in metadata["options"]):
            raise ValueError(f"Option {name!r} is already configured")

        metadata["options"].insert(0, {
            "name": name,
            "description": description,
            "type": option_type,
            "required": required,
            "choices": list(choices) if choices is not None else None,
            "min_value": min_value,
            "max_value": max_value,
            "min_length": min_length,
            "max_length": max_length
        })

        return callback

    return decorator

def cooldown(rate, per, scope = "user"):
    if not isinstance(rate, int) or isinstance(rate, bool) or rate < 1:
        raise ValueError("RATE must be a positive integer")

    if not isinstance(per, (int, float)) or isinstance(per, bool) or per <= 0:
        raise ValueError("PER must be a positive number")

    if scope not in ("user", "guild", "channel", "global"):
        raise ValueError("Unsupported cooldown scope")

    def decorator(callback):
        metadata = _get_metadata(callback)

        if metadata["cooldown"] is not None:
            raise ValueError("Cooldown is already configured")

        metadata["cooldown"] = {
            "rate": rate,
            "per": per,
            "scope": scope
        }

        return callback

    return decorator

def _get_command_metadata(callback):
    metadata = getattr(callback, _JDE_COMMAND_METADATA, None)

    if metadata is None or not metadata["is_command"]:
        raise ValueError("Callback is not decorated with @command")

    return {
        **metadata,
        "options": [dict(item) for item in metadata["options"]],
        "permissions": dict(metadata["permissions"]),
        "bot_permissions": dict(metadata["bot_permissions"]),
        "checks": list(metadata["checks"]),
        "cooldown": dict(metadata["cooldown"]) if metadata["cooldown"] is not None else None
    }

__all__ = [
    "_get_command_metadata",
    "bot_has_permissions",
    "checks",
    "command",
    "cooldown",
    "guild_only",
    "has_permissions",
    "is_owner",
    "option"
]
