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

from typing import final as _final

from jardiscordengine.interns.base_classe import JDEInternBaseClass as _JDEInternBaseClass
from jardiscordengine.interns.decorators import documentation as _documentation

@_documentation
@_final
class JDEBool(_JDEInternBaseClass):

    _instances = {}

    __instance_policy__ = "flyweight"
    __instance_limit__ = 2
    __recursive__ = False

    def __new__(cls, value):
        val = bool(value)

        if val not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[val] = instance

        return cls._instances[val]

    def __init__(self, value):
        if hasattr(self, "_initialized"):
            return

        super().__init__()
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

    def __or__(self, other):
        return JDEBool(self or other)

    def __and__(self, other):
        return JDEBool(self and other)

    @property
    def b(self):
        return bool(self)
