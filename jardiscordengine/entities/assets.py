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

import re

from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.high_classes import (
    JDEInternEntityFieldName as _JDEInternEntityFieldName,
)
from jardiscordengine.interns.high_classes import (
    JDEInternEntityFieldURL as _JDEInternEntityFieldURL,
)
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity


@_documented
class JDEEntityEmoji(_JDEInternEntity, _JDEInternEntityFieldName):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, emoji, name = None, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else name,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, emoji, **kwargs):
        _assert_is_instance(emoji, str, "EMOJI must be str")

        _JDEInternEntity.__init__(self)

        self._emoji = emoji

        unicode_match = re.fullmatch(r":([a-zA-Z0-9_]+):", emoji)
        guild_match = re.fullmatch(
            r"<:([a-zA-Z0-9_]+):(\d{17,20})>",
            emoji,
        )
        animated_match = re.fullmatch(
            r"<a:([a-zA-Z0-9_]+):(\d{17,20})>",
            emoji,
        )

        if unicode_match:
            name = unicode_match.group(1)
            self._guild_id = None
            self._animated = False

        elif guild_match:
            name = guild_match.group(1)
            self._guild_id = int(guild_match.group(2))
            self._animated = False

        elif animated_match:
            name = animated_match.group(1)
            self._guild_id = int(animated_match.group(2))
            self._animated = True

        else:
            raise _JTKExternError.JErrorValue(
                "Emoji format is invalid"
            )

        _JDEInternEntityFieldName.__init__(self, name)

    @property
    def emoji(self):
        return self._emoji

    @property
    def guild_id(self):
        return self._guild_id

    @property
    def animated(self):
        return self._animated

    @classmethod
    def from_emoji(cls, emoji):
        return cls(emoji, _jde_key=emoji)

    @classmethod
    def from_name(cls, name):
        return cls(f":{name}:", _jde_key=f":{name}:")

    @classmethod
    def from_guild(cls, name, guild):
        emoji = f"<:{name}:{guild.id}>"
        return cls(emoji, _jde_key=emoji)

    @classmethod
    def animated_from_guild(cls, name, guild):
        emoji = f"<a:{name}:{guild.id}>"
        return cls(emoji, _jde_key=emoji)

@_documented
class JDEEntityCustomEmoji(JDEEntityEmoji):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documented
class JDEEntityImage(_JDEInternEntity, _JDEInternEntityFieldURL, _JDEInternEntityFieldName):

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
        _JDEInternEntityFieldURL.__init__(self, url)
        _JDEInternEntityFieldName.__init__(self, name)

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
