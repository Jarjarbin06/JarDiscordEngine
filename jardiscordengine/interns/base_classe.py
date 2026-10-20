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
# Licence: GPL v3
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

from math import inf as _inf
from typing import Any as _Any
from uuid import uuid4 as _uuid4

from jardiscordengine.interns import JTKExternConsole as _JTKExternConsole
from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns.decorators import documentation as _documentation
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import warning as _warning

_JDE_WARNED_INSTANCE_LIMIT: set[_Any] = set()

class _JDEInternMeta(type):

    def __call__(cls, *args, **kwargs):
        init_kwargs = kwargs.copy()
        init_kwargs.pop("_jde_warn", None)

        instance = cls.__new__(cls, *args, **kwargs)

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

@_documentation
class JDEInternBaseClass(metaclass=_JDEInternMeta):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = True

    _jde_instances: dict[type, dict[_Any, object]] = {}

    def __new__(
            cls,
            *args,
            _jde_key=None,
            _jde_warn=None,
            **kwargs,
        ):
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
                cls,
                policy,
                key,
            )

            if warning_identifier not in _JDE_WARNED_INSTANCE_LIMIT:
                _JDE_WARNED_INSTANCE_LIMIT.add(warning_identifier)

                _warning(
                    _JTKExternError.JErrorRuntime(
                        f"{cls.__name__}: construction warning for "
                        f"the {policy.upper()} policy."
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

    @staticmethod
    def _get_warning_identifier(cls, policy, key):
        if policy in (
            _JDEInternInstancePolicy.FLYWEIGHT,
            _JDEInternInstancePolicy.UNIQUE,
        ):
            return (cls, key)

        return cls

    @classmethod
    def validate_instance_policies(cls) -> None:
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

        def get_value(value: _Any) -> _Any:
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

        COLOR_THEME: dict[str, tuple[int, int, int]] = {
            "class": (180, 220, 255),
            "attribute": (255, 200, 120),
            "value": (200, 200, 200),
            "engine_object": (120, 255, 180),
            "container": (120, 180, 255),
            "id": (255, 120, 120),
            "name": (255, 255, 150),
            "list": (200, 160, 255),
            "dict": (160, 255, 220),
            "discord": (255, 140, 255),
            "immutable": (180, 180, 180),
            "callable": (255, 180, 100),
            "error": (255, 80, 80),
            "policy": (255, 180, 255),
            "limit": (180, 255, 255),
        }

        BRANCH = "│   "
        SPACE = "    "

        if _visited is None:
            _visited = set()

        if _stack is None:
            _stack = set()

        def _rgb(
                rgb: tuple[int, int, int],
                text: str
            ) -> str:
            return _JTKExternConsole.Text(text).f_color_foreground(_JTKExternConsole.ColorRGB(*rgb))

        def colorize(
                text: str,
                category: str
            ) -> str:
            if not is_colored:
                return text
            color = COLOR_THEME.get(category)
            if color is None:
                return text
            return _rgb(color, text)

        def get_instance_indicator(cls) -> str:
            policy = getattr(
                cls,
                "__instance_policy__",
                _JDEInternInstancePolicy.NORMAL,
            )
            limit = getattr(cls, "__instance_limit__", None)

            if policy == _JDEInternInstancePolicy.NORMAL:
                return f"{{{policy}:∞}}"

            if policy == _JDEInternInstancePolicy.SINGLETON:
                return f"{{{policy}:1}}"

            if policy == _JDEInternInstancePolicy.FLYWEIGHT:
                return f"{{{policy}:{limit}}}"

            if policy == _JDEInternInstancePolicy.UNIQUE:
                return f"{{{policy}:∞}}"

            return ""

        def get_name(obj):
            name = getattr(obj, "name", None)

            if name is not None:
                return name

            for attr_name in dir(obj):
                if "name" in attr_name.lower():
                    value = getattr(obj, attr_name, None)

                    if value is not None:
                        return value

            return None

        def classify(
                name: str,
                value
            ) -> str:
            if name == "JDEID":
                return "id"
            if isinstance(value, JDEInternBaseClass):
                return "engine_object"
            if callable(value):
                return "callable"
            if isinstance(value, dict):
                return "dict"
            if isinstance(value, (list, tuple, set)):
                return "list"
            module_name = getattr(type(value), "__module__", "")
            if "discord" in module_name:
                return "discord"
            return "value"

        def extend_prefix(
                current_prefix: str,
                last_item: bool
            ) -> str:
            return current_prefix + (SPACE if last_item else BRANCH)

        def safe_repr(value) -> str:
            try:
                return repr(value)
            except Exception as err:
                return f"<repr error: {err}>"

        def append_child_object(
                label: str,
                child,
                child_prefix: str,
                last_item: bool
            ):
            connector = "└─ " if last_item else "├─ "
            cls_col = colorize(child.__class__.__name__, "engine_object")
            lines.append(f"{child_prefix}{connector}{label} ({cls_col})")
            if max_depth == 0:
                lines.append(f"{child_prefix}{SPACE if last_item else BRANCH} [...]")
                return

            lines.extend(
                child.debug(
                    is_colored=is_colored,
                    max_depth=max_depth - 1,
                    branched_recursive=branched_recursive,
                    show_root=False,
                    _is_last=True,
                    _is_root=False,
                    _prefix=extend_prefix(child_prefix, last_item),
                    _visited=_visited,
                    _stack=_stack,
                ).splitlines()
            )

        def append_leaf(
                name: str,
                label: str,
                value,
                child_prefix: str,
                last_item: bool
            ):
            connector = "└─ " if last_item else "├─ "
            category = classify(name, value)
            rendered = safe_repr(value)

            module_name = getattr(type(value), "__module__", "")
            if "discord" in module_name:
                rendered = f"{type(value).__name__} (Discord)"
                category = "discord"

            lines.append(
                f"{child_prefix}{connector}{label} = {colorize(rendered, category)}"
            )

        def append_mapping(
                name: str,
                label: str,
                mapping: dict,
                child_prefix: str,
                last_item: bool
            ):
            connector = "└─ " if last_item else "├─ "
            lines.append(f"{child_prefix}{connector}{label} = {colorize('{}', 'dict')}")

            nested_prefix = extend_prefix(child_prefix, last_item)
            items = list(mapping.items())

            for index, (sub_key, sub_value) in enumerate(items):
                sub_last = index == len(items) - 1
                sub_label = colorize(str(sub_key), "name")

                if isinstance(sub_value, JDEInternBaseClass):
                    append_child_object(sub_label, sub_value, nested_prefix, sub_last)
                else:
                    append_leaf(name, sub_label, sub_value, nested_prefix, sub_last)

        def append_sequence(
                name: str,
                label: str,
                sequence,
                child_prefix: str,
                last_item: bool
            ):
            connector = "└─ " if last_item else "├─ "
            lines.append(f"{child_prefix}{connector}{label} = {colorize('[]', 'list')}")

            nested_prefix = extend_prefix(child_prefix, last_item)
            items = list(sequence)

            for index, sub_value in enumerate(items):
                sub_last = index == len(items) - 1
                sub_label = colorize(f"[{index}]", "list")

                if isinstance(sub_value, JDEInternBaseClass):
                    append_child_object(sub_label, sub_value, nested_prefix, sub_last)
                else:
                    append_leaf(name, sub_label, sub_value, nested_prefix, sub_last)

        obj_id = id(self)
        if obj_id in _stack:
            return (
                f"{_prefix}└─ {colorize('<recursive>', 'error')} "
                f"{colorize(self.__class__.__name__, 'class')} ({colorize(f"JDEID-{self.jdeid}" if hasattr(self, "jdeid") else f"ID-{obj_id}", 'id')})"
            )

        if self.__recursive__:
            _stack.add(obj_id)

        try:
            lines: list[str] = []

            name = get_name(self)
            class_name_raw = self.__class__.__name__
            class_name = colorize(class_name_raw, "class")

            indicator = get_instance_indicator(self.__class__)
            indicator = f" {colorize(indicator, 'policy')}" if indicator else ""

            if name:
                base = f"{colorize(name, 'name')} ({class_name})"
            else:
                base = class_name

            label = f"{base}{indicator}"

            if _is_root and show_root:
                lines.append(label)
            else:
                connector = "└─ " if _is_last else "├─ "
                lines.append(f"{_prefix}{connector}{label}")

            new_prefix = extend_prefix(_prefix, _is_last)

            public_attrs = {
                key: value
                for key, value in getattr(self, "__dict__", {}).items()
                if not key.startswith("_")
            }

            props: dict[str, object] = {}
            for attr_name in dir(self.__class__):
                attr = getattr(self.__class__, attr_name, None)
                if isinstance(attr, property) and not attr_name.startswith("_"):
                    try:
                        props[f"@{attr_name}"] = getattr(self, attr_name)
                    except NotImplementedError:
                        props[f"@{attr_name}"] = "<error: not implemented>"
                    except Exception as err:
                        props[f"@{attr_name}"] = f"<error: {err}>"

            all_attrs = {**public_attrs, **props}

            if "@jdeid" in all_attrs:
                append_leaf("JDEID", colorize("JDEID", "id"), all_attrs["@jdeid"], new_prefix, len(all_attrs) == 1)
                all_attrs.pop("@jdeid")

            for index, (attr_name, attr_value) in enumerate(all_attrs.items()):
                last_item = index == len(all_attrs) - 1
                attr_label = colorize(attr_name, "attribute")

                if attr_name == "@jdeid":
                    continue

                if isinstance(attr_value, JDEInternBaseClass):
                    append_child_object(attr_label, attr_value, new_prefix, last_item)
                elif isinstance(attr_value, dict):
                    append_mapping(attr_name, attr_label, attr_value, new_prefix, last_item)
                elif isinstance(attr_value, (list, tuple, set)):
                    append_sequence(attr_name, attr_label, attr_value, new_prefix, last_item)
                else:
                    append_leaf(attr_name, attr_label, attr_value, new_prefix, last_item)

            return "\n".join(lines)
        finally:
            if branched_recursive:
                _stack.discard(obj_id)

    def dump(self, *, _is_last=True, _is_root=True, _prefix="", _attr_key=None, _visited=None):
        BRANCH = "│   "
        SPACE = "    "
        TEE = "├─ "
        ELBOW = "└─ "

        if _visited is None:
            _visited = set()

        def extend_prefix(current: str, last: bool) -> str:
            return current + (SPACE if last else BRANCH)

        def type_name(v) -> str:
            return type(v).__name__

        def get_name(obj):
            name = getattr(obj, "name", None)

            if name is not None:
                return name

            for attr_name in dir(obj):
                if "name" in attr_name.lower():
                    value = getattr(obj, attr_name, None)

                    if value is not None:
                        return value

            return None

        def safe_repr(v) -> str:
            try:
                r = repr(v)
                return r if len(r) <= 80 else r[:77] + "…"
            except Exception:
                return "<repr error>"

        def summarize_collection(v) -> str:
            if isinstance(v, dict):
                if not v:
                    return "dict[0]"
                contained = sorted({type(x).__name__ for x in v.values()})
                return f"dict[{len(v)}] of {', '.join(contained)}"
            try:
                elements = list(v)
            except Exception:
                return f"{type_name(v)}(?)"
            if not elements:
                return f"{type_name(v)}[0]"
            contained = sorted({type(x).__name__ for x in elements})
            return f"{type_name(v)}[{len(elements)}] of {', '.join(contained)}"

        obj_id = id(self)
        if obj_id in _visited and self.__recursive__:
            connector = ELBOW if _is_last else TEE
            key_part = f"{_attr_key}: " if _attr_key else ""
            return f"{_prefix}{connector}{key_part}<circular> {self.__class__.__name__}"
        _visited.add(obj_id)

        lines = []
        class_name = self.__class__.__name__
        name = get_name(self)

        class_part = class_name + (f" ({name!r})" if name else "")

        if _is_root:
            lines.append(class_part)
        else:
            connector = ELBOW if _is_last else TEE
            key_part = f"{_attr_key}: " if _attr_key else ""
            lines.append(f"{_prefix}{connector}{key_part}{class_part}")

        new_prefix = extend_prefix(_prefix, _is_last)

        raw_attrs: dict = {k: v for k, v in dict(getattr(self, "__dict__", {})).items() if not k.startswith("_")}

        props: dict = {}
        for attr_name in dir(self.__class__):
            descriptor = getattr(self.__class__, attr_name, None)
            if isinstance(descriptor, property) and not attr_name.startswith("_"):
                try:
                    props[f"@{attr_name}"] = getattr(self, attr_name)
                except Exception as exc:
                    props[f"@{attr_name}"] = f"<error: {exc}>"

        items = list({**raw_attrs, **props}.items())

        for i, (k, v) in enumerate(items):
            last = (i == len(items) - 1)
            connector = ELBOW if last else TEE

            if isinstance(v, JDEInternBaseClass):
                if id(v) in _visited:
                    lines.append(
                        f"{new_prefix}{connector}{k}: {v.__class__.__name__} = <circular>"
                    )
                else:
                    child = v.dump(
                        _is_last=last,
                        _is_root=False,
                        _prefix=new_prefix,
                        _attr_key=k,
                        _visited=_visited,
                    )
                    lines.append(child)

            elif isinstance(v, (list, tuple, dict)):
                summary = summarize_collection(v)
                lines.append(f"{new_prefix}{connector}{k}: {type_name(v)} = {summary}")

            else:
                lines.append(f"{new_prefix}{connector}{k}: {type_name(v)} = {safe_repr(v)}")

            if last:
                lines.append(f"{new_prefix}")

        lines = [line for line in lines if line.strip()]

        return "\n".join(lines)
