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

from __future__ import annotations

import inspect as _inspect
import time as _time
from collections import defaultdict as _defaultdict
from collections import deque as _deque
from functools import wraps as _wraps
from typing import final as _final

import discord as _discord

from jardiscordengine.commands.decorators import (
    _get_command_metadata,
)
from jardiscordengine.commands.decorators import command as _command
from jardiscordengine.entities.commands import (
    JDEEntityApplicationContext as _JDEEntityApplicationContext,
)
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass as _JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import flag as _flag
from jardiscordengine.interns.decorators import logged as _logged
from jardiscordengine.interns.decorators import register_entity as _register_entity
from jardiscordengine.interns.decorators import requires_init as _requires_init
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)


@_final
@_logged
@_documented
@_register_entity(name="JDECommandManager", category="Manager")
class JDECommandManager(_JDEInternBaseClass):

    __instance_policy__ = _JDEInternInstancePolicy.SINGLETON
    __instance_limit__ = 1
    __recursive__ = True

    @_requires_init
    def __new__(cls, *args, _jde_key = None, _jde_warn = None, **kwargs):
        return _JDEInternBaseClass.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    @_requires_init
    def __init__(self, bot):
        _JDEInternBaseClass.__init__(self)

        self._bot = bot
        self._commands = {}
        self._cooldowns = _defaultdict(_deque)

        self.register_commands(self._ping, self._about, self._help)

    @staticmethod
    @_command("ping", "Check the bot's latency.")
    async def _ping(bot, ctx):
        latency = bot.discord.latency * 1000  # pyright: ignore[reportAttributeAccessIssue]

        await ctx.respond(
            f"Pong! Latency: `{latency:.2f} ms`"
        )

    @staticmethod
    @_command("about", "Display information about the bot and JarDiscordEngine.")
    async def _about(bot, ctx):
        bot_name = (
            bot.discord.user.name
            if bot.discord.user is not None
            else bot.name
        )
        bot_version = bot.version
        bot_description = bot.description

        embed = _discord.Embed(
            title=f"About {bot_name}",
            description=(
                "A Discord bot powered by **JarDiscordEngine**.\n\n"
                "JarDiscordEngine is a lightweight Discord bot framework "
                "built on top of Pycord, designed to simplify bot "
                "development through command management, event handling, "
                "and extensibility."
            ),
            color=_discord.Color.blurple(),
        )

        embed.add_field(
            name="Bot",
            value=bot_name,
            inline=True,
        )
        embed.add_field(
            name="Bot Version",
            value=str(bot_version),
            inline=True,
        )
        embed.add_field(
            name="Bot Description",
            value=str(bot_description),
            inline=True,
        )
        embed.add_field(
            name="Framework",
            value="JarDiscordEngine",
            inline=True,
        )
        embed.add_field(
            name="JDE Version",
            value=__import__(
                "jardiscordengine"
            ).__version__,
            inline=True,
        )

        embed.set_footer(
            text="Powered by JarDiscordEngine"
        )

        await ctx.respond(embed=embed)

    @staticmethod
    @_command("help", "List the commands available to you.")
    async def _help(bot, ctx):
        command_manager = bot.command_manager  # pyright: ignore[reportAttributeAccessIssue]
        available_commands = []

        for name, registered_command in command_manager.commands.items():
            metadata = _get_command_metadata(
                registered_command.callback
            )

            if metadata["guild_only"] and ctx.guild is None:
                continue

            if metadata["owner_only"] and not await command_manager._check_owner(ctx):
                    continue

            if not await command_manager._check_permissions(
                ctx,
                metadata["permissions"],
            ):
                continue

            if not await command_manager._check_permissions(
                ctx,
                metadata["bot_permissions"],
                bot=True,
            ):
                continue

            if not await command_manager._check_custom_checks(
                ctx,
                metadata["checks"],
            ):
                continue

            available_commands.append(
                f"`/{name}` — {metadata['description']}"
            )

        embed = _discord.Embed(
            title="Available Commands",
            description=(
                "\n".join(available_commands)
                if available_commands
                else "You don't have access to any commands."
            ),
            color=_discord.Color.blurple(),
        )

        embed.set_footer(
            text=f"{len(available_commands)} command(s) available"
        )

        await ctx.respond(embed=embed)

    @_flag(doc="Bot")
    def bot(self):
        return "_bot"

    @_flag(doc="Commands")
    def commands(self):
        return "_commands"

    @staticmethod
    def _validate_callback(callback):
        if not callable(callback):
            raise TypeError("CALLBACK must be callable")

        if not _inspect.iscoroutinefunction(callback):
            raise TypeError("COMMAND CALLBACK must be asynchronous")

        parameters = list(
            _inspect.signature(callback).parameters.values()
        )

        if len(parameters) < 2:
            raise TypeError(
                "COMMAND CALLBACK must accept bot and context arguments."
            )

        for parameter in parameters[:2]:
            if parameter.kind not in (
                _inspect.Parameter.POSITIONAL_ONLY,
                _inspect.Parameter.POSITIONAL_OR_KEYWORD,
            ):
                raise TypeError(
                    "The first two command callback parameters must "
                    "accept positional arguments (bot and context)."
                )

    @staticmethod
    def _resolve_option_type(option_type):
        option_types = {
            str: str,
            int: int,
            float: float,
            bool: bool,
            "user": _discord.User,
            "channel": _discord.abc.GuildChannel,
            "role": _discord.Role,
            "mentionable": _discord.abc.Mentionable,
            "attachment": _discord.Attachment,
        }

        if option_type not in option_types:
            raise TypeError(
                f"Unsupported command option type: {option_type!r}."
            )

        return option_types[option_type]

    @staticmethod
    def _validate_options(callback, metadata):
        signature = _inspect.signature(callback)
        parameters = signature.parameters

        if not parameters:
            raise TypeError(
                "COMMAND CALLBACK must accept an application context."
            )

        for option in metadata["options"]:
            option_name = option["name"]

            if option_name not in parameters:
                raise ValueError(
                    f"Command option {option_name!r} does not match "
                    "a parameter in the callback signature."
                )

            parameter = parameters[option_name]

            if parameter.kind not in (
                _inspect.Parameter.POSITIONAL_OR_KEYWORD,
                _inspect.Parameter.KEYWORD_ONLY,
            ):
                raise ValueError(
                    f"Command option {option_name!r} must correspond "
                    "to a named callback parameter."
                )

            if not option["required"] and parameter.default is _inspect.Parameter.empty:
                raise ValueError(
                    f"Optional command option {option_name!r} "
                    "must have a default value in the callback."
                )

    @staticmethod
    def _create_options(metadata):
        options = []

        for option in metadata["options"]:
            option_type = JDECommandManager._resolve_option_type(
                option["type"]
            )

            options.append(
                _discord.Option(
                    option_type,
                    description=option["description"],
                    name=option["name"],
                    required=option["required"],
                    choices=option["choices"],
                    min_value=option["min_value"],
                    max_value=option["max_value"],
                    min_length=option["min_length"],
                    max_length=option["max_length"],
                )
            )

        return options

    @staticmethod
    def _validate_permissions(permissions):
        supported_permissions = _discord.Permissions.VALID_FLAGS

        for name, value in permissions.items():
            if name not in supported_permissions:
                raise ValueError(
                    f"Unsupported Discord permission: {name!r}."
                )

            if not isinstance(value, bool):
                raise TypeError(
                    f"Permission {name!r} must be bool."
                )

    async def _deny(self, context, message):
        await context.respond(message, ephemeral=True)

    async def _check_permissions(self, context, permissions, *, bot=False):
        if not permissions:
            return True

        guild = context.guild

        if guild is None:
            return False

        if bot:
            member = guild.me

            if member is None:
                return False

            current_permissions = member.guild_permissions
        else:
            current_permissions = context.user.guild_permissions

        for name, expected in permissions.items():
            if getattr(current_permissions, name) != expected:
                return False

        return True

    async def _check_custom_checks(self, context, callbacks):
        for callback in callbacks:
            result = callback(context)

            if _inspect.isawaitable(result):
                result = await result

            if not isinstance(result, bool):
                raise TypeError(
                    "Custom command checks must return bool."
                )

            if not result:
                return False

        return True

    async def _check_owner(self, context):
        return await self._bot.discord.is_owner(context.user)

    @staticmethod
    def _cooldown_key(context, scope):
        if scope == "user":
            return context.user.id

        if scope == "guild":
            return context.guild_id

        if scope == "channel":
            return context.channel_id

        return None

    def _check_cooldown(self, command_name, context, cooldown):
        if cooldown is None:
            return True

        rate = cooldown["rate"]
        per = cooldown["per"]
        scope = cooldown["scope"]

        key = (
            command_name,
            scope,
            self._cooldown_key(context, scope),
        )

        now = _time.monotonic()
        timestamps = self._cooldowns[key]

        while timestamps and now - timestamps[0] >= per:
            timestamps.popleft()

        if len(timestamps) >= rate:
            return False

        timestamps.append(now)

        return True

    async def _execute_command(self, callback, metadata, context, *args, **kwargs):
        if metadata["guild_only"] and context.guild is None:
            await self._deny(
                context,
                "This command can only be used in a server.",
            )
            return

        if metadata["owner_only"] and not await self._check_owner(context):
            await self._deny(
                context,
                "Only the bot owner can use this command.",
            )
            return

        if not await self._check_permissions(
            context,
            metadata["permissions"],
        ):
            await self._deny(
                context,
                "You do not have the required permissions.",
            )
            return

        if not await self._check_permissions(
            context,
            metadata["bot_permissions"],
            bot=True,
        ):
            await self._deny(
                context,
                "The bot does not have the required permissions.",
            )
            return

        if not await self._check_custom_checks(
            context,
            metadata["checks"],
        ):
            await self._deny(
                context,
                "You cannot use this command.",
            )
            return

        if not self._check_cooldown(
            metadata["name"],
            context,
            metadata["cooldown"],
        ):
            await self._deny(
                context,
                "This command is on cooldown.",
            )
            return

        return await callback(self._bot, context, *args, **kwargs)

    def register_command(self, callback):
        self._validate_callback(callback)

        metadata = _get_command_metadata(callback)

        if not metadata["is_command"]:
            raise ValueError(
                "Callback is not decorated with @command."
            )

        name = metadata["name"]

        if name in self._commands:
            raise ValueError(
                f"Command {name!r} is already registered."
            )

        self._validate_permissions(metadata["permissions"])
        self._validate_permissions(metadata["bot_permissions"])
        self._validate_options(callback, metadata)

        options = self._create_options(metadata)

        @_wraps(callback)
        async def command_callback(context, *args, **kwargs):
            jde_context = _JDEEntityApplicationContext(context)

            return await self._execute_command(
                callback,
                metadata,
                jde_context,
                *args,
                **kwargs,
            )

        callback_parameters = _inspect.signature(callback).parameters
        command_parameters = [
            _inspect.Parameter(
                "context",
                kind=_inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]

        for option in metadata["options"]:
            parameter = callback_parameters[option["name"]]

            command_parameters.append(
                parameter.replace(
                    name=option["name"],
                )
            )

        command_callback.__signature__ = _inspect.Signature(  # pyright: ignore[reportAttributeAccessIssue]
            parameters=command_parameters,
        )

        registered_command = self._bot.discord.slash_command(
            name=name,
            description=metadata["description"],
            options=options,
            guild_only=metadata["guild_only"],
        )(command_callback)

        self._commands[name] = registered_command

        return registered_command

    def register_commands(self, *callbacks):
        registered_commands = []

        for callback in callbacks:
            registered_commands.append(
                self.register_command(callback)
            )

        return registered_commands

    def get_command(self, name):
        if not isinstance(name, str):
            raise TypeError("NAME must be str")

        return self._commands.get(name)

    def unregister_command(self, name):
        if not isinstance(name, str):
            raise TypeError("NAME must be str")

        command = self._commands.pop(name, None)

        if command is None:
            raise LookupError(
                f"Command {name!r} is not registered."
            )

        self._bot.discord.remove_application_command(
            command.name,
        )

        cooldown_keys = [
            key
            for key in self._cooldowns
            if key[0] == name
        ]

        for key in cooldown_keys:
            self._cooldowns.pop(key, None)

        return command

__all__ = [
    "JDECommandManager",
]
