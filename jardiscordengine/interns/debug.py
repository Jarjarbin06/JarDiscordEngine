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
from dataclasses import dataclass as _dataclass
from enum import Enum as _Enum

from jardiscordengine.interns import JTKExternConsole as _JTKExternConsole
from jardiscordengine.interns import JTKExternTime as _JTKExternTime
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import field as _field
from jardiscordengine.interns.decorators import flag as _flag
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)

_DEBUG_EXCLUDED_INHERITANCE_MODULES = (
    "jardiscordengine.interns.low_classes",
)

_DEBUG_THEME: dict[str, tuple[int, int, int]] = {
    # header
    "class": (180, 220, 255),
    "name": (255, 255, 150),
    "policy": (255, 180, 255),
    "decorators": (190, 255, 120),
    # row labels
    "id": (255, 120, 120),
    "property": (100, 210, 255),
    "flag": (190, 255, 120),
    "field": (120, 230, 200),
    "attribute": (255, 200, 120),
    "method": (190, 160, 255),
    # values
    "engine_object": (120, 255, 180),
    "callable": (255, 180, 100),
    "dict": (160, 255, 220),
    "list": (200, 160, 255),
    "extern": (255, 140, 255),
    "true": (130, 255, 150),
    "false": (255, 130, 130),
    "none": (150, 150, 150),
    "string": (255, 225, 170),
    "number": (130, 190, 255),
    "value": (200, 200, 200),
    # misc
    "error": (255, 80, 80),
    "dim": (130, 130, 130),
    # commands
    "discord_command": (100, 200, 255),
    "terminal_command": (255, 180, 100),
}

_DEBUG_ICONS: dict[str, str] = {
    "id": "#",
    "property": "⚙",
    "flag": "⚐",
    "field": "⏵",
    "attribute": "◈",
    "method": "ƒ",
}

_DEBUG_SKIPPED_MEMBERS = frozenset({
    "jdeid",
    "debug",
    "doc",
    "to_dict",
    "validate_instance_policies",
})

_DEBUG_BAR = "│"
_DEBUG_BRANCH = "│   "
_DEBUG_SPACE = "    "
_DEBUG_TEE = "├─ "
_DEBUG_END = "└─ "

@_dataclass(frozen = True)
class _DebugError:
    message: str

    def __str__(self):
        return f"<error: {self.message}>"

@_dataclass(frozen = True)
class _DebugMethod:
    signature: str
    return_type: str
    decorators: tuple[str, ...]

def _debug_command_candidates(obj):
    """Yield an object and its underlying callbacks when available."""
    seen = set()
    pending = [obj]

    while pending:
        candidate = pending.pop(0)

        if candidate is None or id(candidate) in seen:
            continue

        seen.add(id(candidate))
        yield candidate

        for attribute in ("callback", "func", "__wrapped__"):
            try:
                wrapped = getattr(candidate, attribute, None)
            except Exception:  # noqa: BLE001, S112
                continue

            if wrapped is not None and wrapped is not candidate:
                pending.append(wrapped)


def _debug_discord_command(obj):
    from jardiscordengine.commands.decorators import (
        _get_command_metadata,
    )

    for candidate in _debug_command_candidates(obj):
        try:
            metadata = _get_command_metadata(candidate)
        except (TypeError, ValueError, AttributeError):
            continue

        if (
            metadata.get("is_command")
            and isinstance(metadata.get("name"), str)
            and isinstance(metadata.get("description"), str)
        ):
            return metadata

    return None

def _debug_terminal_command(obj):
    for candidate in _debug_command_candidates(obj):
        name = getattr(candidate, "cmd_name", None)
        description = getattr(candidate, "cmd_description", None)
        arguments = getattr(candidate, "cmd_arguments", None)

        if (
            isinstance(name, str)
            and isinstance(description, str)
            and isinstance(arguments, tuple)
        ):
            return {
                "name": name,
                "description": description,
                "arguments": arguments,
            }

    return None

def _debug_command_header(obj, paint):
    metadata = _debug_discord_command(obj)

    if metadata is not None:
        name = metadata["name"]
        description = metadata["description"]

        return (
            f"{paint('Command', 'discord_command')} - "
            f"{paint(name, 'name')} "
            f"{paint(f'({description})', 'string')}"
        )

    metadata = _debug_terminal_command(obj)

    if metadata is not None:
        name = metadata["name"]
        arguments = metadata["arguments"]

        formatted_arguments = ", ".join(
            f"{argument[0]}: {argument[1]}"
            for argument in arguments
        )

        return (
            f"{paint('TerminalCommand', 'terminal_command')} - "
            f"{paint(name, 'name')} "
            f"{paint(f'({formatted_arguments})', 'string')}"
        )

    return None

def _debug_painter(is_colored):
    if not is_colored:
        return lambda text, role: str(text)

    def paint(text, role):
        rgb = _DEBUG_THEME.get(role)
        if rgb is None:
            return str(text)
        return str(
            _JTKExternConsole.Text(str(text)).f_color_foreground(
                _JTKExternConsole.ColorRGB(*rgb)
            )
        )

    return paint

def _debug_extend(prefix, last):
    return prefix + (_DEBUG_SPACE if last else _DEBUG_BRANCH)

def _debug_safe_get(obj, name):
    try:
        return getattr(obj, name)
    except NotImplementedError:
        return _DebugError("not implemented")
    except Exception as err:  # noqa: BLE001
        return _DebugError(f"{type(err).__name__}({err})")

def _debug_decorator_names(target):
    metadata = getattr(target, "__jde_decorators__", None) or ()
    return tuple(
        str(item.get("name", item.get("decorator_name", item)))
        if isinstance(item, dict)
        else str(item)
        for item in metadata
    )

def _debug_decorators_text(names, paint):
    return paint(f"‖ {', '.join(names)} ‖", "decorators") if names else ""

def _debug_inheritance_text(cls, paint):
    classes = [
        base.__name__[3:]
        for base in cls.__mro__
        if (
            base.__name__.startswith("JDE")
            and base.__name__ != "JDEDebug"
            and base.__module__ not in _DEBUG_EXCLUDED_INHERITANCE_MODULES
        )
    ]

    return paint(f"[ {' > '.join(classes)} ]", "dim")

def _debug_instance_indicator(cls):
    policy = getattr(cls, "__instance_policy__", _JDEInternInstancePolicy.NORMAL)
    limit = getattr(cls, "__instance_limit__", None)

    if policy in (
        _JDEInternInstancePolicy.NORMAL,
        _JDEInternInstancePolicy.UNIQUE,
    ):
        shown = "∞"
    elif policy == _JDEInternInstancePolicy.SINGLETON:
        shown = "1"
    elif policy == _JDEInternInstancePolicy.FLYWEIGHT:
        shown = str(limit)
    else:
        return ""

    return f"{{{policy.name}:{shown}}}"

def _debug_find_name(obj):
    name = _debug_safe_get(obj, "name")
    if name is not None and not isinstance(name, _DebugError):
        return name

    for attr_name in dir(obj):
        if attr_name.startswith("_") or "name" not in attr_name.lower():
            continue
        value = _debug_safe_get(obj, attr_name)
        if value is None or isinstance(value, _DebugError) or callable(value):
            continue
        return value

    return None

def _debug_header(obj, paint):
    command_header = _debug_command_header(obj, paint)

    if command_header is not None:
        return command_header

    cls = type(obj)
    class_text = paint(cls.__name__, "class")
    name = _debug_find_name(obj)

    base = f"{paint(name, 'name')} ({class_text})" if name else class_text

    indicator = _debug_instance_indicator(cls)
    indicator = f"{paint(indicator, 'policy')}" if indicator else ""

    decorators = _debug_decorators_text(_debug_decorator_names(cls), paint)

    inheritance = _debug_inheritance_text(cls, paint)

    return f"{base} {indicator} {decorators} {inheritance}"

def _debug_describe_method(obj, name):
    method = getattr(obj, name)
    decorators = _debug_decorator_names(method)

    try:
        signature = _inspect.signature(method)
    except (TypeError, ValueError):
        return _DebugMethod("(...)", "", decorators)

    annotation = signature.return_annotation
    if annotation is _inspect.Signature.empty:
        return_type = ""
    elif isinstance(annotation, str):
        return_type = annotation
    else:
        return_type = getattr(annotation, "__name__", str(annotation))

    params = str(signature.replace(return_annotation=_inspect.Signature.empty))

    return _DebugMethod(params, return_type, decorators)

def _debug_is_pycord_callable(value):
    if not callable(value):
        return False

    module = getattr(value, "__module__", None)

    if module is None:
        module = getattr(
            getattr(value, "__func__", None),
            "__module__",
            None,
        )

    return (
        isinstance(module, str)
        and (
            module == "discord"
            or module.startswith("discord.")
        )
    )

def _debug_collect_rows(obj):
    cls = type(obj)
    properties = []
    flags = []
    fields = []
    attributes = []
    methods = []

    for name in dir(cls):
        if name.startswith("_") or name in _DEBUG_SKIPPED_MEMBERS:
            continue

        attr = getattr(cls, name, None)

        if isinstance(attr, property):
            properties.append(("property", name, _debug_safe_get(obj, name)))

        elif isinstance(attr, _flag):
            flags.append(("flag", name, _debug_safe_get(obj, name)))

        elif isinstance(attr, _field):
            fields.append(("field", name, _debug_safe_get(obj, name)))

        elif _inspect.isroutine(attr) or isinstance(attr, (classmethod, staticmethod)):
            try:
                methods.append(("method", name, _debug_describe_method(obj, name)))
            except Exception as err:  # noqa: BLE001
                methods.append(
                    ("method", name, _DebugError(f"{type(err).__name__}({err})"))
                )

        else:
            value = _debug_safe_get(obj, name)
            if _inspect.isroutine(value):
                try:
                    value = _inspect.signature(value)
                except (TypeError, ValueError):
                    pass
            attributes.append(("attribute", name, value))

    jdeid = getattr(obj, "jdeid", None)
    if jdeid is None:
        jdeid = _DebugError("failed to load JDEID")

    return [
        ("id", "JDEID", jdeid),
        *properties,
        *flags,
        *fields,
        *attributes,
        *methods,
    ]

def _debug_role(value):
    from jardiscordengine.constants import JDEFalse as _JDEFalse
    from jardiscordengine.constants import JDETrue as _JDETrue
    from jardiscordengine.interns.base_classe import (
        JDEInternBaseClass as _JDEInternBaseClass,
    )

    if isinstance(value, _DebugError):
        return "error"
    elif value is True or value is _JDETrue:
        return "true"
    elif value is False or value is _JDEFalse:
        return "false"
    elif isinstance(value, _JDEInternBaseClass):
        return "engine_object"
    elif (
        isinstance(value, _JTKExternTime.Time) or
        "discord" in getattr(type(value), "__module__", "") or
        _debug_is_pycord_callable(value)
    ):
        return "extern"
    elif value is None:
        return "none"
    elif isinstance(value, _inspect.Signature) or callable(value):
        return "callable"
    elif isinstance(value, dict):
        return "dict"
    elif isinstance(value, (list, tuple, set)):
        return "list"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, (int, float)):
        return "number"
    else:
        return "value"

def _debug_render(value):
    from jardiscordengine.systems.bool import JDEBool as _JDEBool

    if isinstance(value, _DebugError | _JDEBool):
        return str(value)
    elif isinstance(value, _inspect.Signature):
        return f"Function {value}"
    elif _debug_is_pycord_callable(value):
        try:
            signature = _inspect.signature(value)
        except (TypeError, ValueError):
            signature = "(...)"

        return f"Function {signature} (Extern:PyCord)"
    elif isinstance(value, _Enum):
        return f"{value.name} (Enum:{value.__class__.__name__})"
    elif isinstance(value, _JTKExternTime.Time):
        return f"{type(value).__name__} <{value}> (Extern:JarbinToolKit:Time)"
    elif "discord" in getattr(type(value), "__module__", ""):
        return f"{type(value).__name__} (Extern:PyCord)"
    else:
        try:
            return repr(value)
        except Exception as err:  # noqa: BLE001
            return f"<repr error: {err}>"

class _DebugWriter:

    def __init__(self, *, is_colored, max_depth, branched_recursive, stack, column):
        self.is_colored = is_colored
        self.max_depth = max_depth
        self.branched_recursive = branched_recursive
        self.stack = stack
        self.column = column
        self.paint = _debug_painter(is_colored)
        self.lines: list[str] = []

    def line(self, prefix, last, text):
        self.lines.append(f"{prefix}{_DEBUG_END if last else _DEBUG_TEE}{text}")

    def separator(self, prefix):
        self.lines.append(f"{prefix}{_DEBUG_BAR}")

    def label(self, prefix, text, role):
        used = len(prefix) + len(_DEBUG_TEE) + len(text)
        padding = max(0, self.column - used)
        return f"{self.paint(text, role)}{' ' * padding}"

    def row(self, prefix, last, role, name, value):
        text = f"{_DEBUG_ICONS[role]} : {name}"

        if isinstance(value, _DebugMethod):
            signature = value.signature
            if value.return_type:
                signature += f" -> {value.return_type}"
            decorators = _debug_decorators_text(value.decorators, self.paint)
            self.line(
                prefix,
                last,
                f"{self.paint(text, role)} {self.paint(signature, 'callable')}"
                f"{f' {decorators}' if decorators else ''}",
            )
        elif role == "id":
            value_role = "error" if isinstance(value, _DebugError) else "id"
            self.line(
                prefix,
                last,
                f"{self.label(prefix, text, role)} = {self.paint(value, value_role)}",
            )
        else:
            self.value(prefix, last, text, role, value)

    def value(self, prefix, last, text, role, value, *, nested = False):
        from jardiscordengine.interns.base_classe import (
            JDEInternBaseClass as _JDEInternBaseClass,
        )
        from jardiscordengine.systems.bool import JDEBool as _JDEBool

        label = self.label(prefix, text, role)

        command_header = _debug_command_header(value, self.paint)

        if command_header is not None:
            self.line(prefix, last, f"{label} = {command_header}")
        elif isinstance(value, _JDEInternBaseClass) and not isinstance(value, _JDEBool):
            self._engine_object(prefix, last, label, value)
        elif not nested and isinstance(value, dict):
            items = [(str(k), "name", v) for k, v in value.items()]
            self._container(prefix, last, label, "{}", "dict", items)
        elif not nested and isinstance(value, (list, tuple, set)):
            items = [(f"[{i}]", "list", v) for i, v in enumerate(value)]
            self._container(prefix, last, label, "[]", "list", items)
        else:
            rendered = self.paint(_debug_render(value), _debug_role(value))
            self.line(prefix, last, f"{label} = {rendered}")

    def _container(self, prefix, last, label, brackets, role, items):
        count = f" ({len(items)})" if items else " (empty)"
        self.line(
            prefix,
            last,
            f"{label} = {self.paint(brackets, role)}{self.paint(count, 'dim')}",
        )

        nested_prefix = _debug_extend(prefix, last)
        for index, (sub_text, sub_role, sub_value) in enumerate(items):
            self.value(
                nested_prefix,
                index == len(items) - 1,
                sub_text,
                sub_role,
                sub_value,
                nested=True,
            )

    def _engine_object(self, prefix, last, label, child):
        header = _debug_header(child, self.paint)

        if id(child) in self.stack:
            self.line(prefix, last, f"{label} = {self.paint('<recursive>', 'error')} {header}")
            return

        self.line(prefix, last, f"{label} = {header}")

        if self.max_depth == 0:
            self.line(_debug_extend(prefix, last), True, self.paint("[...]", "dim"))
            return

        text = child.debug(
            is_colored=self.is_colored,
            max_depth=self.max_depth - 1,
            branched_recursive=self.branched_recursive,
            show_root=False,
            _is_last=last,
            _is_root=False,
            _prefix=prefix,
            _stack=self.stack,
        )
        self.lines.extend(text.splitlines())

@_documented
class JDEDebug:

    __recursive__ = True

    def debug(self, *, is_colored = False, max_depth = -1, branched_recursive = False, show_root = True, _is_last = True, _is_root = True, _prefix = "", _visited = None, _stack = None):

        paint = _debug_painter(is_colored)
        stack: set[int] = _stack if _stack is not None else set()
        obj_id = id(self)

        if obj_id in stack:
            jdeid = getattr(self, "jdeid", None)
            ident = f"JDEID-{jdeid}" if jdeid else f"ID-{obj_id}"
            return (
                f"{_prefix}{_DEBUG_END}{paint('<recursive>', 'error')} "
                f"{paint(type(self).__name__, 'class')} ({paint(ident, 'id')})"
            )

        if self.__recursive__:
            stack.add(obj_id)

        try:
            lines: list[str] = []

            if show_root:
                header = _debug_header(self, paint)
                lines.append(
                    header
                    if _is_root
                    else f"{_prefix}{_DEBUG_END if _is_last else _DEBUG_TEE}{header}"
                )

            body_prefix = _debug_extend(_prefix, _is_last)
            rows = _debug_collect_rows(self)

            width = max(
                (
                    len(f"{_DEBUG_ICONS[role]} : {name}")
                    for role, name, _ in rows
                    if role != "method"
                ),
                default=0,
            )

            writer = _DebugWriter(
                is_colored=is_colored,
                max_depth=max_depth,
                branched_recursive=branched_recursive,
                stack=stack,
                column=len(body_prefix) + len(_DEBUG_TEE) + width,
            )

            previous_role = None

            for index, (role, name, value) in enumerate(rows):
                if previous_role is not None and role != previous_role:
                    writer.separator(body_prefix)

                previous_role = role
                writer.row(body_prefix, index == len(rows) - 1, role, name, value)

            lines.extend(writer.lines)
            return "\n".join(lines)
        finally:
            if branched_recursive:
                stack.discard(obj_id)

__all__ = [
    "JDEDebug",
]
