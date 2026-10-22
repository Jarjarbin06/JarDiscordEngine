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

from typing import final as _final

from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass as _JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import documentation as _documentation
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)


@_documentation
@_final
class JDEBool(_JDEInternBaseClass):

    __instance_policy__ = _JDEInternInstancePolicy.FLYWEIGHT
    __instance_limit__ = 2
    __recursive__ = False

    def __new__(cls, value, _jde_key = None, _jde_warn = None):
        return _JDEInternBaseClass.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else bool(value),
            _jde_warn=_jde_warn if _jde_warn is not None else False,
        )

    def __init__(self, value):
        if hasattr(self, "_initialized"):
            return

        _JDEInternBaseClass.__init__(self)

        self._bool = bool(value)
        self._initialized = True

    def __bool__(self):
        return self._bool

    def __int__(self):
        return int(self._bool)

    def __str__(self):
        return "JETrue" if self else "JEFalse"

    def __repr__(self):
        return f"<{self}>"

    def __call__(self):
        return JDEBool(not self)

    def __and__(self, other):
        return JDEBool(bool(self) and bool(other))

    def __or__(self, other):
        return JDEBool(bool(self) or bool(other))

    @property
    def b(self):
        return bool(self)
