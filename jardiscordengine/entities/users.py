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

from jardiscordengine.entities.guilds import JDEGuilds as _JDEGuilds
from jardiscordengine.interns.enums import JDEInternInstancePolicy as _JDEInternInstancePolicy
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.high_classes import JDEInternUserIdentity as _JDEInternUserIdentity
from jardiscordengine.interns.decorators import documentation as _documentation

@_documentation
class JDEUser(_JDEInternUserIdentity):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, id, username, _jde_key = None):
        return _JDEInternUserIdentity.__new__(
            cls,
            id,
            username,
            _jde_key=_jde_key or id
        )

    def __init__(self, id, username):
        _JDEInternUserIdentity.__init__(self, id, username)

@_documentation
class JDEClientUser(JDEUser):

    __instance_policy__ = _JDEInternInstancePolicy.SINGLETON
    __instance_limit__ = 1
    __recursive__ = False

@_documentation
class JDEMember(JDEUser):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, user, guild, _jde_key = None):
        return JDEUser.__new__(
            cls,
            user.id,
            user.username,
            _jde_key=_jde_key or user.id
        )

    def __init__(self, user, guild):
        _assert_is_instance(user, JDEUser, "USER must be JDEUser")
        _assert_is_instance(guild, _JDEGuilds, "GUILD must be JDEGuilds")

        JDEUser.__init__(self, user.id, user.username)

        self._guild = guild

    @property
    def guild(self):
        return self._guild

@_documentation
class JDEUserProfile(_JDEInternUserIdentity):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, user, _jde_key = None):
        return _JDEInternUserIdentity.__new__(
            cls,
            user.id,
            user.username,
            _jde_key=_jde_key or user.id
        )

    def __init__(self, user):
        _assert_is_instance(user, JDEUser, "USER must be JDEUser")

        _JDEInternUserIdentity.__init__(self, user.id, user.username)

        self._user = user

    @property
    def user(self):
        return self._user
