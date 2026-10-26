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
from math import inf as _inf
from typing import Any as _Any
from typing import ClassVar as _ClassVar
from uuid import uuid4 as _uuid4

from jardiscordengine.interns import JTKExternConsole as _JTKExternConsole
from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns import JTKExternTime as _JTKExternTime
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import field as _field
from jardiscordengine.interns.decorators import flag as _flag
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import warning as _warning

_JDE_WARNED_INSTANCE_LIMIT: set[_Any] = set()

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
    return paint(f" | {', '.join(names)} |", "decorators") if names else ""

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
    cls = type(obj)
    class_text = paint(cls.__name__, "class")
    name = _debug_find_name(obj)

    base = f"{paint(name, 'name')} ({class_text})" if name else class_text

    indicator = _debug_instance_indicator(cls)
    indicator = f" {paint(indicator, 'policy')}" if indicator else ""

    decorators = _debug_decorators_text(_debug_decorator_names(cls), paint)

    return f"{base}{indicator}{decorators}"

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

def _debug_collect_rows(obj):
    cls = type(obj)
    properties = []
    values = []
    methods = []

    for name in dir(cls):
        if name.startswith("_") or name in _DEBUG_SKIPPED_MEMBERS:
            continue

        attr = getattr(cls, name, None)

        if isinstance(attr, property):
            properties.append(("property", name, _debug_safe_get(obj, name)))

        elif isinstance(attr, _flag):
            values.append(("flag", name, _debug_safe_get(obj, name)))

        elif isinstance(attr, _field):
            values.append(("field", name, _debug_safe_get(obj, name)))

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
            values.append(("attribute", name, value))

    jdeid = getattr(obj, "jdeid", None)
    if jdeid is None:
        jdeid = _DebugError("failed to load JDEID")

    return [("id", "JDEID", jdeid), *properties, *values, *methods]

def _debug_role(value):
    if isinstance(value, _DebugError):
        return "error"
    if isinstance(value, JDEInternBaseClass):
        return "engine_object"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "none"
    if isinstance(value, _inspect.Signature) or callable(value):
        return "callable"
    if isinstance(value, dict):
        return "dict"
    if isinstance(value, (list, tuple, set)):
        return "list"
    if isinstance(value, _JTKExternTime.Time) or "discord" in getattr(
        type(value), "__module__", ""
    ):
        return "extern"
    if isinstance(value, str):
        return "string"
    if isinstance(value, (int, float)):
        return "number"
    return "value"

def _debug_render(value):
    if isinstance(value, _DebugError):
        return str(value)
    if isinstance(value, _inspect.Signature):
        return f"Function {value}"
    if isinstance(value, _JTKExternTime.Time):
        return f"{type(value).__name__} <{value}> (JarbinToolKit:Time)"
    if "discord" in getattr(type(value), "__module__", ""):
        return f"{type(value).__name__} (PyCord)"

    try:
        return repr(value)
    except Exception as err:  # noqa: BLE001
        return f"<repr error: {err}>"

class _DebugWriter:
    def __init__(self, *, is_colored, max_depth, branched_recursive, stack):
        self.is_colored = is_colored
        self.max_depth = max_depth
        self.branched_recursive = branched_recursive
        self.stack = stack
        self.paint = _debug_painter(is_colored)
        self.lines: list[str] = []

    def line(self, prefix, last, text):
        self.lines.append(f"{prefix}{_DEBUG_END if last else _DEBUG_TEE}{text}")

    def row(self, prefix, last, role, name, value):
        label = self.paint(f"{_DEBUG_ICONS[role]} : {name}", role)

        if isinstance(value, _DebugMethod):
            signature = value.signature
            if value.return_type:
                signature += f" -> {value.return_type}"
            self.line(
                prefix,
                last,
                f"{label} {self.paint(signature, 'callable')}"
                f"{_debug_decorators_text(value.decorators, self.paint)}",
            )
        elif role == "id":
            self.line(prefix, last, f"{label} = {self.paint(value, 'error' if isinstance(value, _DebugError) else 'id')}")
        else:
            self.value(prefix, last, label, value)

    def value(self, prefix, last, label, value, *, nested = False):
        if isinstance(value, JDEInternBaseClass):
            self._engine_object(prefix, last, label, value)
        elif not nested and isinstance(value, dict):
            items = [(self.paint(str(k), "name"), v) for k, v in value.items()]
            self._container(prefix, last, label, "{}", "dict", items)
        elif not nested and isinstance(value, (list, tuple, set)):
            items = [(self.paint(f"[{i}]", "list"), v) for i, v in enumerate(value)]
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
        for index, (sub_label, sub_value) in enumerate(items):
            self.value(
                nested_prefix,
                index == len(items) - 1,
                sub_label,
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

class _JDEInternMeta(type):

    def __call__(cls, *args, **kwargs):
        init_kwargs = kwargs.copy()
        init_kwargs.pop("_jde_warn", None)

        instance = cls.__new__(cls, *args, **kwargs)  # pyright: ignore[reportCallIssue, reportArgumentType]

        if not isinstance(instance, cls):
            return instance

        if getattr(instance, "_jde_initialized", False):
            return instance

        instance._jde_initialized = True

        try:
            cls.__init__(instance, *args, **init_kwargs)
        except Exception:
            instance._jde_initialized = False
            raise

        return instance

@_documented
class JDEInternBaseClass[PolicyT: _JDEInternInstancePolicy, LimitT: int, RecursiveT: bool](metaclass=_JDEInternMeta):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = True

    _jde_instances: _ClassVar[dict[type, dict[_Any, object]]] = {}

    def __new__(cls, *args, _jde_key=None, _jde_warn=None, **kwargs):
        if _jde_key is None:
            _jde_key = True

        policy = cls.__instance_policy__
        limit = cls.__instance_limit__

        if policy == _JDEInternInstancePolicy.NORMAL:
            return object.__new__(cls)

        instances = JDEInternBaseClass._jde_instances.setdefault(cls, {})

        if policy == _JDEInternInstancePolicy.SINGLETON:
            key = None

        elif policy in (
            _JDEInternInstancePolicy.FLYWEIGHT,
            _JDEInternInstancePolicy.UNIQUE,
        ):
            if _jde_key is None:
                raise _JTKExternError.JErrorRuntime(
                    f"{cls.__name__} requires an explicit _jde_key "
                    f"when using the {policy} policy."
                )
            key = _jde_key

        else:
            raise _JTKExternError.JErrorValue(
                f"Invalid instance policy {policy!r} "
                f"for {cls.__name__}."
            )

        exists = key in instances

        should_warn = (
            policy == _JDEInternInstancePolicy.SINGLETON and exists
            or policy == _JDEInternInstancePolicy.UNIQUE and exists
            or (
                policy == _JDEInternInstancePolicy.FLYWEIGHT
                and not exists
                and len(instances) >= limit
            )
        )

        if should_warn and _jde_warn:
            warning_identifier = cls._get_warning_identifier(
                policy,
                key,
            )

            if warning_identifier not in _JDE_WARNED_INSTANCE_LIMIT:
                _JDE_WARNED_INSTANCE_LIMIT.add(warning_identifier)

                _warning(
                    _JTKExternError.JErrorRuntime(
                        f"{cls.__name__}: construction warning for "
                        f"the {policy.name} policy."
                    )
                )

        if exists:
            return instances[key]

        instance = object.__new__(cls)
        instances[key] = instance

        if (
            policy == _JDEInternInstancePolicy.FLYWEIGHT
            and len(instances) > limit
        ):
            del instances[key]
            raise _JTKExternError.JErrorRuntime(
                f"{cls.__name__} reached its instance limit "
                f"of {limit}."
            )

        return instance

    @classmethod
    def _get_warning_identifier(cls, policy, key):
        if policy in (
            _JDEInternInstancePolicy.FLYWEIGHT,
            _JDEInternInstancePolicy.UNIQUE,
        ):
            return (cls, key)

        return cls

    @classmethod
    def validate_instance_policies(cls):
        policy = cls.__instance_policy__
        limit = cls.__instance_limit__

        if not isinstance(policy, _JDEInternInstancePolicy):
            raise _JTKExternError.JErrorValue(
                f"{cls.__name__}: invalid instance policy {policy!r}."
            )

        if (
            isinstance(limit, bool)
            or not isinstance(limit, (int, float))
            or limit < 0
            or limit == _inf
        ):
            raise _JTKExternError.JErrorValue(
                f"{cls.__name__}: instance limit must be a "
                "finite, non-negative number."
            )

        if policy == _JDEInternInstancePolicy.NORMAL:
            if limit != 0:
                raise _JTKExternError.JErrorValue(
                    f"{cls.__name__}: normal policy requires "
                    "an instance limit of 0."
                )

        elif policy == _JDEInternInstancePolicy.SINGLETON:
            if limit != 1:
                raise _JTKExternError.JErrorValue(
                    f"{cls.__name__}: singleton requires "
                    "an instance limit of 1."
                )

        elif policy == _JDEInternInstancePolicy.FLYWEIGHT:
            if limit < 1:
                raise _JTKExternError.JErrorValue(
                    f"{cls.__name__}: flyweight requires "
                    "an instance limit of at least 1."
                )

        elif policy == _JDEInternInstancePolicy.UNIQUE and limit != 0:
            raise _JTKExternError.JErrorValue(
                f"{cls.__name__}: unique requires "
                "an instance limit of 0."
            )

    def __init__(self):
        self._jdeid: str = _uuid4().hex

    @property
    def jdeid(self):
        return self._jdeid

    @jdeid.setter
    def jdeid(self, value):
        raise _JTKExternError.JErrorValue("JDEID must not be changed")

    def __str__(self):
        id = getattr(self, "jdeid", None)

        return f"{self.__class__.__name__}({id=})"

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(jdeid={getattr(self, 'jdeid', 'unknown')})>"
        )

    def to_dict(self):

        def get_value(value: _Any):
            if isinstance(value, JDEInternBaseClass):
                return value.to_dict()
            else:
                return value

        return {
            "class": self.__class__.__name__,
            "jdeid": self.jdeid,
            "public": {
                k: get_value(v)
                for k, v in self.__dict__.items()
                if not k.startswith("_") and not callable(v)
            }
        }

    def debug(self, *, is_colored = False, max_depth = -1, branched_recursive = False, show_root = True, _is_last = True, _is_root = True, _prefix = "", _visited = None, _stack = None):

        paint = _debug_painter(is_colored)
        stack: set[int] = _stack if _stack is not None else set()
        obj_id = id(self)

        # Cycle detected on the entry object itself.
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

            writer = _DebugWriter(
                is_colored=is_colored,
                max_depth=max_depth,
                branched_recursive=branched_recursive,
                stack=stack,
            )

            body_prefix = _debug_extend(_prefix, _is_last)
            rows = _debug_collect_rows(self)

            for index, (role, name, value) in enumerate(rows):
                writer.row(body_prefix, index == len(rows) - 1, role, name, value)

            lines.extend(writer.lines)
            return "\n".join(lines)
        finally:
            if branched_recursive:
                stack.discard(obj_id)

__all__ = [
    "JDEInternBaseClass",
]
