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

import os as _os

from dotenv import load_dotenv as _load_dotenv

from jardiscordengine.interns.extern import JTKExternError as _JTKExternError

_MISSING = object()

class JDEEnvMeta(type):

    @classmethod
    def __call__(cls, setting, default = _MISSING):
        try:
            return _os.environ.get(setting)
        except ValueError as err:
            if default is not _MISSING:
                return default
            raise _JTKExternError.JErrorValue() from err

class JDEEnv(metaclass=JDEEnvMeta):

    @staticmethod
    def load(path = None):
        _load_dotenv(path)

    @staticmethod
    def set(setting, value):
        _os.environ[setting] = str(value)

    @staticmethod
    def contains(setting):
        return setting in _os.environ

__all__ = [
    "JDEEnv",
]
