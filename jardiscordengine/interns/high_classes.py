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

from jardiscordengine.interns.enums import JDEInternInstancePolicy as _JDEInternInstancePolicy
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity
from jardiscordengine.interns.decorators import documentation as _documentation

@_documentation
class JDEInternIdentity(_JDEInternEntity):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, id, _jde_key = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key or id,
        )

    def __init__(self, id):
        _assert_is_instance(id, int, "ID must be int")

        _JDEInternEntity.__init__(self)

        self._id = id

    @property
    def id(self):
        return self._id

@_documentation
class JDEInternUserIdentity(JDEInternIdentity):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, id, username, _jde_key = None):
        return JDEInternIdentity.__new__(
            cls,
            id,
            _jde_key=_jde_key or id,
        )

    def __init__(self, id, username):
        _assert_is_instance(username, str, "USERNAME must be str")

        JDEInternIdentity.__init__(self, id)

        self._username = username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        _assert_is_instance(username, str, "USERNAME must be str")

        self._username = username

@_documentation
class JDEInternAsset(_JDEInternEntity):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, name, _jde_key = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key,
        )

    def __init__(self, name):
        _assert_is_instance(name, str, "NAME must be str")

        _JDEInternEntity.__init__(self)

        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        _assert_is_instance(name, str, "NAME must be str")

        self._name = name
