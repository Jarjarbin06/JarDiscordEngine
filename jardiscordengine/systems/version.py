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
from enum import (
    IntEnum as _IntEnum,
    auto as _auto,
)

from jardiscordengine.interns.base_classe import JDEInternBaseClass as _JDEInternBaseClass
from jardiscordengine.interns.decorators import documentation as _documentation
from jardiscordengine.interns.enums import JDEInternInstancePolicy as _JDEInternInstancePolicy
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance

@_final
@_documentation
class JDECompatibility(_IntEnum):

    OK = _auto()
    WARNING = _auto()
    ERROR = _auto()

@_documentation
class JDEVersion(_JDEInternBaseClass):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    fields = ("major", "minor", "patch")

    def __new__(cls, major, minor, patch, _jde_key = None):
        return _JDEInternBaseClass.__new__(
            cls,
            _jde_key=_jde_key
        )

    def __init__(self, major, minor, patch):
        _assert_is_instance(major, int, "MAJOR must be int")
        _assert_is_instance(minor, int, "MINOR must be int")
        _assert_is_instance(patch, int, "PATCH must be int")

        _JDEInternBaseClass.__init__(self)

        self._version = (major, minor, patch)

    def __repr__(self):
        fields = (
            f"{name}={value}"
            for name, value in zip(self.fields, self._version)
        )

        return f"<{self.__class__.__name__}({', '.join(fields)})>"

    def __str__(self):
        return ".".join(str(value) for value in self._version)

    def __iter__(self):
        return iter(self._version)

    def __getitem__(self, index):
        return self._version[index]

    @property
    def major(self):
        return self._version[0]

    @property
    def minor(self):
        return self._version[1]

    @property
    def patch(self):
        return self._version[2]

    def compatibility(
            self,
            other,
        ):
        if not isinstance(other, JDEVersion):
            raise TypeError(
                "'other' must be an instance of JDEVersion."
            )

        if self.major != other.major:
            return JDECompatibility.ERROR

        if self.minor < other.minor:
            return JDECompatibility.ERROR

        if self.minor == other.minor and self.patch < other.patch:
            return JDECompatibility.WARNING

        return JDECompatibility.OK
