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

from jardiscordengine.entities.guilds import JDEEntityGuild as _JDEEntityGuild
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import field as _field
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.high_classes import (
    JDEInternFieldID as _JDEInternFieldID,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldUsername as _JDEInternFieldUsername,
)
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity


@_documented
class JDEEntityUser(_JDEInternEntity, _JDEInternFieldID, _JDEInternFieldUsername):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, id, username, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else id,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, id, username):
        _JDEInternEntity.__init__(self)
        _JDEInternFieldID.__init__(self, id)
        _JDEInternFieldUsername.__init__(self, username)

@_documented
class JDEEntityClientUser(JDEEntityUser):

    __instance_policy__ = _JDEInternInstancePolicy.SINGLETON
    __instance_limit__ = 1
    __recursive__ = False

@_documented
class JDEEntityMember(JDEEntityUser):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    guild = _field(_JDEEntityGuild, required=True, read_only=True, doc="Discord guild")

    def __new__(cls, user, guild, _jde_key = None, _jde_warn = None):
        return JDEEntityUser.__new__(
            cls,
            user.id,
            user.username,
            _jde_key=_jde_key if _jde_key is not None else (user.id, guild.id),
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, user, guild):
        _assert_is_instance(user, JDEEntityUser, "USER must be JDEEntityUser")

        JDEEntityUser.__init__(self, user.id, user.username)

        self.guild = guild

@_documented
class JDEEntityUserProfile(_JDEInternEntity):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    user = _field(JDEEntityUser, required=True, read_only=True, doc="Discord user")

    def __new__(cls, user, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else user.id,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, user):
        _assert_is_instance(user, JDEEntityUser, "USER must be JDEEntityUser")

        _JDEInternEntity.__init__(self)

        self.user = user
