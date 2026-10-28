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

from math import inf as _inf
from typing import Any as _Any
from typing import ClassVar as _ClassVar
from uuid import uuid4 as _uuid4

from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns.debug import JDEDebug as _JDEDebug
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import warning as _warning

_JDE_WARNED_INSTANCE_LIMIT: set[_Any] = set()

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
class JDEInternBaseClass[PolicyT: _JDEInternInstancePolicy, LimitT: int, RecursiveT: bool](_JDEDebug, metaclass=_JDEInternMeta):

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

__all__ = [
    "JDEInternBaseClass",
]
