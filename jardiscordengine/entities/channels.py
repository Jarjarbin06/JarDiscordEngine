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

from discord.abc import GuildChannel as _GuildChannel

from jardiscordengine.entities.guilds import JDEEntityGuild as _JDEEntityGuild
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import field as _field
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.high_classes import (
    JDEInternFieldDiscord as _JDEInternFieldDiscord,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldID as _JDEInternFieldID,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldName as _JDEInternFieldName,
)
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity


@_documented
class JDEEntityChannel(_JDEInternEntity, _JDEInternFieldID, _JDEInternFieldName):

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
        _JDEInternFieldID.__init__(self, id)
        _JDEInternFieldName.__init__(self, name)

@_documented
class JDEEntityGuildChannel(JDEEntityChannel, _JDEInternFieldDiscord):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    guild = _field(_JDEEntityGuild, required=True, read_only=True, doc="Discord guild")

    def __new__(cls, channel, guild, _jde_key = None, _jde_warn = None):
        return JDEEntityChannel.__new__(
            cls,
            channel.id,
            channel.name,
            _jde_key=_jde_key if _jde_key is not None else channel.id,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, channel, guild):
        _assert_is_instance(channel, _GuildChannel, "CHANNEL must be discord.abc.GuildChannel")
        _assert_is_instance(guild, _JDEEntityGuild, "GUILD must be JDEEntityGuild")

        JDEEntityChannel.__init__(self, channel.id, channel.name)
        _JDEInternFieldDiscord.__init__(self, channel)

        self.guild = guild

    async def send(self, content: str):
        return await self.discord.send(content)  # pyright: ignore[reportAttributeAccessIssue]

@_documented
class JDEEntityTextChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntityVoiceChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntityStageChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntityForumChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntityAnnouncementChannel(JDEEntityGuildChannel):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False
