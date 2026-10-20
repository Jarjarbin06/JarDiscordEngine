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

from jardiscordengine.entities.guilds import JDEEntityGuild as _JDEEntityGuild
from jardiscordengine.interns.decorators import documentation as _documentation
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.high_classes import (
    JDEInternEntityFieldID as _JDEInternEntityFieldID,
)
from jardiscordengine.interns.high_classes import (
    JDEInternEntityFieldName as _JDEInternEntityFieldName,
)
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity


@_documentation
class JDEEntityChannel(_JDEInternEntity, _JDEInternEntityFieldID, _JDEInternEntityFieldName):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, id, name, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else id,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, id, name):
        _JDEInternEntity.__init__(self)
        _JDEInternEntityFieldID.__init__(self, id)
        _JDEInternEntityFieldName.__init__(self, name)

@_documentation
class JDEEntityGuildChannel(JDEEntityChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, channel, guild, _jde_key = None, _jde_warn = None):
        return JDEEntityChannel.__new__(
            cls,
            channel.id,
            channel.name,
            _jde_key=_jde_key if _jde_key is not None else (channel.id, guild.id),
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, channel, guild):
        _assert_is_instance(channel, JDEEntityChannel, "CHANNEL must be JDEEntityChannel")
        _assert_is_instance(guild, _JDEEntityGuild, "GUILD must be JDEEntityGuild")

        JDEEntityChannel.__init__(self, channel.id, channel.name)

        self._guild = guild

    @property
    def guild(self):
        return self._guild

@_documentation
class JDEEntityTextChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
class JDEEntityVoiceChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
class JDEEntityStageChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
class JDEEntityForumChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
class JDEEntityAnnouncementChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False
