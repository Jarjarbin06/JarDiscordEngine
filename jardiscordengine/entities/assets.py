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
from jardiscordengine.interns.decorators import documentation as _documentation
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity
from jardiscordengine.interns.high_classes import (
    JDEInternEntityFieldName as _JDEInternEntityFieldName,
    JDEInternEntityFieldURL as _JDEInternEntityFieldURL
)

@_documentation
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

    def __init__(self, emoji, name = None):
        if name is None:
            name = emoji

        _assert_is_instance(emoji, str, "EMOJI must be str")

        _JDEInternEntity.__init__(self)
        _JDEInternEntityFieldName.__init__(self, name)

        self._emoji = f":{emoji}:"

    @property
    def emoji(self):
        return self._emoji

@_documentation
class JDEEntityCustomEmoji(JDEEntityEmoji):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
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

@_documentation
class JDEEntityAvatar(JDEEntityImage):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
class JDEEntityGuildIcon(JDEEntityImage):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
class JDEEntityBanner(JDEEntityImage):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
class JDEEntitySticker(JDEEntityImage):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False
