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
from jardiscordengine.interns.high_classes import (
    JDEInternFieldName as _JDEInternFieldName,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldURL as _JDEInternFieldURL,
)
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity


@_documented
class JDEEntityEmoji(_JDEInternEntity, _JDEInternFieldName):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    emoji = _field(str, required=True, read_only=True, doc="Emoji")
    name = _field(str, required=True, read_only=True, doc="Name")
    guild = _field(_JDEEntityGuild | None, read_only=True, doc="Guild")
    animated = _field(bool, read_only=True, doc="Is animated")

    def __new__(cls, emoji, name, guild = None, animated = False, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else name,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, emoji, name, guild = None, animated = False, **kwargs):
        _JDEInternEntity.__init__(self)
        _JDEInternFieldName.__init__(self, name)

        self.emoji = emoji
        self.guild = guild
        self.animated = animated

    def __str__(self):
        if self.guild is not None:
            if self.animated:
                return f"<a:{self.emoji}:{self.guild.id}>"

            return f"<:{self.emoji}:{self.guild.id}>"

        return f":{self.emoji}:"

    @classmethod
    def from_emoji(cls, emoji, name):
        return cls(emoji, name)

    @classmethod
    def from_guild(cls, emoji, name, guild):
        return cls(emoji, name, guild)

    @classmethod
    def animated_from_guild(cls, emoji, name, guild):
        return cls(emoji, name, guild, True)

@_documented
class JDEEntityCustomEmoji(JDEEntityEmoji):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntityImage(_JDEInternEntity, _JDEInternFieldURL, _JDEInternFieldName):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, url, name = None, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else name,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, url, name = None):
        if name is None:
            name = url.split("/")[-1]

        _JDEInternEntity.__init__(self)
        _JDEInternFieldURL.__init__(self, url)
        _JDEInternFieldName.__init__(self, name)

@_documented
class JDEEntityAvatar(JDEEntityImage):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntityGuildIcon(JDEEntityImage):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntityBanner(JDEEntityImage):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntitySticker(JDEEntityImage):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False
