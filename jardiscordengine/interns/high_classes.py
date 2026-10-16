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

from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity
from jardiscordengine.interns.decorators import documentation as _documentation

@_documentation
class JDEInternPartialEntity(_JDEInternEntity):

    __instance_policy__ = "normal"
    __instance_limit__ = None
    __recursive__ = False

    def __init__(self, id):
        super().__init__()

        self._id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        raise AttributeError(f"{self.__class__.__name__}.id cannot be changed")

@_documentation
class JDEInternUserIdentity(JDEInternPartialEntity):

    __instance_policy__ = "normal"
    __instance_limit__ = None
    __recursive__ = False

    def __init__(self, id, name):
        super().__init__(id)

        self.name = name

@_documentation
class JDEInternAsset(_JDEInternEntity):

    __instance_policy__ = "normal"
    __instance_limit__ = None
    __recursive__ = False

    def __init__(self, name):
        super().__init__()

        self.name = name
