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

from sys import version_info as _python_version

from discord import __version__ as _discord_version

from jardiscordengine import __config_version__ as _config_version
from jardiscordengine import __version__ as _jardiscordengine_version
from jardiscordengine.systems.bool import JDEBool as _JDEBool
from jardiscordengine.systems.version import JDEVersion as _JDEVersion

# Versions #
JDEVersion_JarDiscordEngine = _JDEVersion(*(int(v) for v in _jardiscordengine_version.split('.')))
JDEVersion_Config = _JDEVersion(*(int(v) for v in _config_version.split(".")))
JDEVersion_Discord = _JDEVersion(*(int(v) for v in _discord_version.split(".")))
JDEVersion_Python = _JDEVersion(*_python_version[0:3])

# Booleans #
JDEFalse = _JDEBool(0)
JDETrue = _JDEBool(1)

__all__ = [  # noqa: RUF022
    # Versions #
    "JDEVersion_JarDiscordEngine",
    "JDEVersion_Config",
    "JDEVersion_Discord",
    "JDEVersion_Python",
    # Booleans #
    "JDEFalse",
    "JDETrue"
]
