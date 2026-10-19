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
from jardiscordengine.interns.high_classes import JDEInternAsset as _JDEInternAsset
from jardiscordengine.interns.decorators import documentation as _documentation

@_documentation
class JDEEmoji(_JDEInternAsset):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, emoji, name = None, _jde_key = None):
        return _JDEInternAsset.__new__(
            cls,
            name,
            _jde_key=_jde_key
        )

    def __init__(self, emoji, name = None):
        if name is None:
            name = emoji

        _assert_is_instance(emoji, str, "EMOJI must be str")

        _JDEInternAsset.__init__(self, name)

        self._emoji = f":{emoji}:"

    @property
    def emoji(self):
        return self._emoji

@_documentation
class JDECustomEmoji(JDEEmoji):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

@_documentation
class JDESticker(_JDEInternAsset):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, url, name = None, _jde_key = None):
        return _JDEInternAsset.__new__(
            cls,
            name,
            _jde_key=_jde_key
        )

    def __init__(self, url, name = None):
        if name is None:
            name = url.split("/")[-1]

        _assert_is_instance(url, str, "URL must be str")

        _JDEInternAsset.__init__(self, name)

        self._url = url

    @property
    def url(self):
        return self._url
