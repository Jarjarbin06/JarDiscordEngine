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

from jardiscordengine.interns.high_classes import JDEInternAsset as _JDEInternAsset
from jardiscordengine.interns.decorators import documentation as _documentation

@_documentation
class JDEEmoji(_JDEInternAsset):

    __instance_policy__ = "normal"
    __instance_limit__ = None
    __recursive__ = False

    def __init__(self, emoji, name = None):
        if name is None:
            name = emoji

        super().__init__(name)

        self._emoji = f":{emoji}:"

    @property
    def emoji(self):
        return self._emoji

    @emoji.setter
    def emoji(self, emoji):
        raise AttributeError(f"{self.__class__.__name__}.emoji cannot be changed")

    def __str__(self):
        return self._emoji

    def __repr__(self):
        return f"{self.__class__.__name__}(emoji={self._emoji!r})"

@_documentation
class JDECustomEmoji(JDEEmoji):

    __instance_policy__ = "normal"
    __instance_limit__ = None
    __recursive__ = False

@_documentation
class JDESticker(_JDEInternAsset):

    __instance_policy__ = "normal"
    __instance_limit__ = None
    __recursive__ = False

    def __init__(self, url, name = None):
        if name is None:
            name = url.split("/")[-1]

        super().__init__(name)

        self._url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        raise AttributeError(f"{self.__class__.__name__}.url cannot be changed")

    def __str__(self):
        return self._url

    def __repr__(self):
        return f"{self.__class__.__name__}(url={self._url!r})"
