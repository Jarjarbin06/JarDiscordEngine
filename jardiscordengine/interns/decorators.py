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
from functools import update_wrapper as _update_wrapper
from functools import wraps as _wraps
from inspect import iscoroutinefunction as _iscoroutinefunction
from threading import RLock as _RLock

from jarbin_toolkit_time import StopWatch as _StopWatch


def _mark_jde_decorator(decorator_target, decorator_name, **metadata):
    decorators = list(getattr(decorator_target, "__jde_decorators__", ()))

    entry = {"decorator_name": decorator_name, **metadata}

    if entry not in decorators:
        decorators.append(entry)  # pyright: ignore[reportArgumentType]

    decorator_target.__jde_decorators__ = tuple(decorators)
    return decorator_target

def documented(cls):

    def get_doc(obj):
        return _inspect.getdoc(obj) or ""

    def annotation_name(annotation):
        if annotation is _inspect.Signature.empty:
            return ""
        if isinstance(annotation, str):
            return annotation
        return getattr(annotation, "__name__", str(annotation))

    def safe_repr(value):
        try:
            return repr(value)
        except Exception:
            return f"<{type(value).__name__}: repr failed>"

    def descriptor_metadata(value):
        metadata = getattr(value, "__jde_field_metadata__", None)
        if metadata is None:
            metadata = getattr(value, "__jde_flag_metadata__", None)
        return dict(metadata) if isinstance(metadata, dict) else {}

    def build_docmap(target_cls):
        result = {
            "class": {
                "name": target_cls.__qualname__,
                "module": target_cls.__module__,
                "doc": get_doc(target_cls),
                "attributes": {},
                "methods": {},
                "properties": {},
                "fields": {},
                "flags": {},
            }
        }
        section = result["class"]

        resolved = {}
        for base in reversed(target_cls.__mro__):
            for name, value in vars(base).items():
                if name.startswith("_"):
                    continue
                resolved[name] = (base, value)

        for name, (owner, value) in resolved.items():
            metadata = descriptor_metadata(value)
            source = owner.__qualname__

            if isinstance(value, property):
                getter = value.fget
                section["properties"][name] = {
                    "doc": get_doc(getter),
                    "read_only": value.fset is None,
                    "type": annotation_name(
                        _inspect.signature(getter).return_annotation
                    ) if getter else "",
                    "defined_in": source,
                }
                continue

            if _inspect.isfunction(value) or _inspect.ismethod(value) or isinstance(
                value, (classmethod, staticmethod)
            ):
                func = value.__func__ if isinstance(
                    value, (classmethod, staticmethod)
                ) else value
                try:
                    signature = _inspect.signature(func)
                    parameters = []
                    for parameter in signature.parameters.values():
                        parameters.append({
                            "name": parameter.name,
                            "kind": parameter.kind.name.lower(),
                            "annotation": annotation_name(parameter.annotation),
                            "default": (
                                "<required>"
                                if parameter.default is _inspect.Parameter.empty
                                else safe_repr(parameter.default)
                            ),
                        })
                    return_annotation = annotation_name(signature.return_annotation)
                    signature_text = str(signature)
                except (TypeError, ValueError):
                    parameters = []
                    return_annotation = ""
                    signature_text = "(...)"
                section["methods"][name] = {
                    "signature": signature_text,
                    "parameters": parameters,
                    "return_type": return_annotation,
                    "doc": get_doc(func),
                    "defined_in": source,
                    "kind": (
                        "classmethod" if isinstance(value, classmethod)
                        else "staticmethod" if isinstance(value, staticmethod)
                        else "method"
                    ),
                }
                continue

            if metadata:
                if metadata.get("kind") == "field":
                    section["fields"][name] = {**metadata, "defined_in": source}
                elif metadata.get("kind") == "flag":
                    section["flags"][name] = {**metadata, "defined_in": source}

            if hasattr(value, "__get__") and not isinstance(
                value, (str, bytes, int, float, bool, tuple, list, dict, set, type(None))
            ):
                continue

            section["attributes"][name] = {
                "type": type(value).__name__,
                "value": safe_repr(value),
                "doc": get_doc(value),
                "defined_in": source,
            }

        return result

    def print_docmap(docmap):
        cls_info = docmap["class"]
        print(f"{cls_info['name']} ({cls_info['module']})")
        print("=" * (len(cls_info["name"]) + len(cls_info["module"]) + 3))
        if cls_info["doc"]:
            print(cls_info["doc"])

        def print_section(title, entries) -> None:
            if not entries:
                return
            print(f"\\n{title}:")
            for name, info in entries.items():
                defined_in = info.get("defined_in")
                suffix = f" [inherited/defined in {defined_in}]" if defined_in else ""
                if title == "Attributes":
                    print(f"  - {name}: {info['type']} = {info['value']}{suffix}")
                    if info.get("doc"):
                        print(f"      {info['doc']}")
                elif title == "Methods":
                    print(f"  - {name}{info['signature']} [{info['kind']}]{suffix}")
                    if info.get("return_type"):
                        print(f"      Returns: {info['return_type']}")
                    if info.get("doc"):
                        print(f"      {info['doc']}")
                elif title == "Properties":
                    access = "read-only" if info["read_only"] else "read/write"
                    print(f"  - {name} [{access}]{suffix}")
                    if info.get("type"):
                        print(f"      Type: {info['type']}")
                    if info.get("doc"):
                        print(f"      {info['doc']}")
                else:
                    print(f"  - {name}{suffix}")
                    for key, value in info.items():
                        if key != "defined_in":
                            print(f"      {key}: {value}")

        print_section("Attributes", cls_info["attributes"])
        print_section("Properties", cls_info["properties"])
        print_section("Fields", cls_info["fields"])
        print_section("Flags", cls_info["flags"])
        print_section("Methods", cls_info["methods"])

    cls.__docmap__ = build_docmap(cls)

    @classmethod
    def doc(documented_cls):
        print_docmap(documented_cls.__docmap__)

    _mark_jde_decorator(cls, "documented")

    cls.doc = doc
    return cls

_ENTITY_REGISTRY = {}
_ENTITY_REGISTRY_LOCK = _RLock()

def register_entity(entity = None, *, name = None, category = "entity", replace = False):

    def decorator(target):
        entity_name = name or target.__name__
        key = (category, entity_name)

        with _ENTITY_REGISTRY_LOCK:
            if key in _ENTITY_REGISTRY and not replace:
                existing = _ENTITY_REGISTRY[key]

                if existing is not target:
                    raise ValueError(
                        f"Entity {entity_name!r} is already registered "
                        f"in category {category!r}"
                    )

            _ENTITY_REGISTRY[key] = target

        _mark_jde_decorator(
            target,
            "register_entity",
            name=entity_name,
            category=category,
        )

        return target

    if entity is None:
        return decorator

    if not callable(entity):
        raise TypeError("register_entity expects a class or callable")

    return decorator(entity)

def _get_jde_log():
    from jardiscordengine.interns.log import log

    return log


def _get_jde_error():
    from jardiscordengine.interns.helpers import error

    return error


def logged(func = None, *, title = "Call", level = "DEBUG", log_args = False):

    def decorator(target):
        @_wraps(target)
        def wrapper(*args, **kwargs):
            log = _get_jde_log()

            description = f"Calling {target.__qualname__}"

            if log_args:
                description += (
                    f" | args={args!r}, kwargs={kwargs!r}"
                )

            log(level, title, description)  # pyright: ignore[reportArgumentType]

            try:
                result = target(*args, **kwargs)
            except Exception as exc:
                log(
                    "ERROR",
                    title,
                    f"{target.__qualname__} raised "
                    f"{type(exc).__name__}: {exc}",
                )
                raise

            log(
                level,  # pyright: ignore[reportArgumentType]
                title,
                f"{target.__qualname__} completed successfully",
            )

            return result

        _mark_jde_decorator(
            wrapper,
            "logged",
            title=title,
            level=level,
            log_args=log_args,
        )

        return wrapper

    if func is None:
        return decorator

    return decorator(func)

def handle_errors(func = None, *, reraise = True, default = None, keyboard_interrupt = False):

    def decorator(target):
        @_wraps(target)
        def wrapper(*args, **kwargs):
            try:
                return target(*args, **kwargs)

            except Exception as exc:
                log = _get_jde_log()
                error = _get_jde_error()

                log(
                    "ERROR",
                    target.__qualname__,
                    f"{type(exc).__name__}: {exc}",
                )

                error(exc)

                if reraise:
                    raise

                return default

        _mark_jde_decorator(
            wrapper,
            "handle_errors",
            reraise=reraise,
            default=repr(default),
        )

        return wrapper

    if func is None:
        return decorator

    return decorator(func)

def deprecated(func = None, *, new_func = None, version = None):

    def decorator(target):
        warned = False

        @_wraps(target)
        def wrapper(*args, **kwargs):
            nonlocal warned

            if not warned:
                if new_func is not None:
                    from jardiscordengine.interns.helpers import (
                        deprecated as deprecated_helper,
                    )

                    deprecated_helper(target, new_func, version)
                else:
                    log = _get_jde_log()
                    message = (
                        f"{target.__qualname__} is deprecated"
                    )

                    if version:
                        message += f" since {version}"

                    log("WARN", "DEPRECATED", message)

                warned = True

            return target(*args, **kwargs)

        wrapper.__deprecated__ = True  # pyright: ignore[reportAttributeAccessIssue]
        wrapper.__deprecated_since__ = version  # pyright: ignore[reportAttributeAccessIssue]
        wrapper.__deprecated_replacement__ = new_func  # pyright: ignore[reportAttributeAccessIssue]

        _mark_jde_decorator(
            wrapper,
            "deprecated",
            version=version,
            replacement=getattr(new_func, "__qualname__", repr(new_func)),
        )

        return wrapper

    if func is None:
        return decorator

    return decorator(func)

def timed(func=None, *, level="DEBUG", title="Timing"):

    def decorator(target):
        if _iscoroutinefunction(target):

            @_wraps(target)
            async def async_wrapper(*args, **kwargs):
                sw = _StopWatch(start=True)

                try:
                    return await target(*args, **kwargs)
                finally:
                    sw.stop()
                    elapsed = sw.elapsed()

                    _get_jde_log()(
                        level,  # pyright: ignore[reportArgumentType]
                        title,
                        f"{target.__qualname__} took {elapsed:.6f} seconds",
                    )

            wrapper = async_wrapper

        else:

            @_wraps(target)
            def sync_wrapper(*args, **kwargs):
                sw = _StopWatch(start=True)

                try:
                    return target(*args, **kwargs)
                finally:
                    sw.stop()
                    elapsed = sw.elapsed()

                    _get_jde_log()(
                        level,  # pyright: ignore[reportArgumentType]
                        title,
                        f"{target.__qualname__} took {elapsed:.6f} seconds",
                    )

            wrapper = sync_wrapper

        _mark_jde_decorator(
            wrapper,
            "timed",
            level=level,
            title=title,
        )

        return wrapper

    if func is None:
        return decorator

    return decorator(func)

def requires_init(func):

    @_wraps(func)
    def wrapper(*args, **kwargs):
        from jardiscordengine import _session

        if _session is None:
            raise RuntimeError(
                f"{func.__qualname__} requires JarDiscordEngine.init() "
                "to be called first"
            )

        return func(*args, **kwargs)

    _mark_jde_decorator(wrapper, "requires_init")

    return wrapper

_MISSING = object()

class field:

    def __init__(self, expected_type = None, *, default = _MISSING, required = False, read_only = False, validator = None, doc = "", storage = None, setter_check = None):
        self.expected_type = expected_type
        self.default = default
        self.required = required
        self.read_only = read_only
        self.validator = validator
        self.doc = doc
        self.storage = storage
        self.setter_check = setter_check
        self.name = ""
        self.owner: type | None = None
        self.__jde_field_metadata__ = {
            "kind": "field",
            "type": self._type_name(expected_type),
            "required": required,
            "read_only": read_only,
            "default": "<missing>" if default is _MISSING else repr(default),
            "validator": getattr(validator, "__name__", repr(validator)) if validator else None,
            "doc": doc,
        }

    @staticmethod
    def _type_name(expected_type):
        if expected_type is None:
            return "Any"
        if isinstance(expected_type, tuple):
            return " | ".join(getattr(item, "__name__", str(item)) for item in expected_type)
        return getattr(expected_type, "__name__", str(expected_type))

    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name
        if self.storage is None:
            self.storage = f"_{name}"
        self.__jde_field_metadata__["name"] = name
        self.__jde_field_metadata__["storage"] = self.storage

    def _default_value(self):
        if self.default is _MISSING:
            raise AttributeError(
                f"{type(self.owner).__name__.upper() if self.owner else 'OBJECT'}."
                f"{self.name} has not been initialized"
            )
        if callable(self.default) and not isinstance(self.default, type):
            return self.default()
        return self.default

    def __get__(self, instance, owner = None):
        if instance is None:
            return self

        assert self.storage is not None

        if not hasattr(instance, self.storage):
            value = self._default_value()
            self._validate(value)
            setattr(instance, self.storage, value)

        return getattr(instance, self.storage)

    def __set__(self, instance, value):
        assert self.storage is not None

        if self.setter_check is not None and not self.setter_check(instance):
            raise AttributeError(
                f"{self.name} can only be set by JDE"
            )

        if (
            not getattr(instance, "_jde_initializing", False)
            and self.read_only
            and hasattr(instance, self.storage)
        ):
            raise AttributeError(f"{self.name} is read-only")

        self._validate(value)
        setattr(instance, self.storage, value)

    def __delete__(self, instance):
        assert self.storage is not None

        if self.setter_check is not None and not self.setter_check(instance):
            raise AttributeError(
                f"{self.name} can only be set by JDE"
            )

        if self.read_only and hasattr(instance, self.storage):
            raise AttributeError(f"{self.name} is read-only")

        if hasattr(instance, self.storage):
            delattr(instance, self.storage)

    def _validate(self, value):
        if self.required and value is None:
            raise ValueError(f"{self.name.upper()} is required and cannot be None")
        if self.expected_type is not None and not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name.upper()} must be {self._type_name(self.expected_type)}, "
                f"got {type(value).__name__}"
            )
        if self.validator is not None and not self.validator(value):
            raise ValueError(f"Invalid value for field {self.name.upper()}: {value!r}")

    def __repr__(self):
        return f"<field name={self.name!r} storage={self.storage!r}>"

class flag:

    def __init__(self, obj = ".", *, name = None, cast = None, doc = ""):
        self.obj = obj
        self.name = name
        self.cast = cast
        self.doc = doc
        self.owner: type | None = None
        self.public_name = ""
        self.__jde_flag_metadata__ = {
            "kind": "flag",
            "target": obj,
            "storage": name,
            "doc": doc,
            "read_only": False,
        }

    def __call__(self, func):
        if self.name is None:
            try:
                self.name = func(None)
            except Exception as exc:
                raise TypeError(
                    "A flag declaration function must return its backing attribute name"
                ) from exc
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("flag backing attribute name must be a non-empty string")
        if not self.doc:
            self.doc = getattr(func, "__doc__", None) or ""
        self.__jde_flag_metadata__.update({
            "storage": self.name,
            "doc": self.doc,
        })
        _update_wrapper(self, func)
        return self

    def __set_name__(self, owner, name):
        self.owner = owner
        self.public_name = name
        self.__jde_flag_metadata__["name"] = name

    def _target(self, instance):
        if self.obj == ".":
            return instance
        return getattr(instance, self.obj)

    def __get__(self, instance, owner = None):
        if instance is None:
            return self

        if self.name is None:
            raise AttributeError(f"flag {self.public_name!r} has no backing attribute")

        value = getattr(self._target(instance), self.name)

        if self.cast:
            return self.cast(value)

        return value

    def __set__(self, instance, value):
        if self.name is None:
            raise AttributeError(f"flag {self.public_name!r} has no backing attribute")
        setattr(self._target(instance), self.name, value)

    def __delete__(self, instance):
        if self.name is None:
            raise AttributeError(f"flag {self.public_name!r} has no backing attribute")
        delattr(self._target(instance), self.name)

    def __repr__(self):
        return (
            f"<flag public_name={self.public_name!r} "
            f"obj={self.obj!r} name={self.name!r}>"
        )

__all__ = [
    "deprecated",
    "documented",
    "field",
    "flag",
    "handle_errors",
    "logged",
    "register_entity",
    "requires_init",
    "timed",
]
