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

import os

os.environ["JARBIN_CONSOLE_NO_BANNER"] = "1"

import discord as DiscordExtern
import jarbin_toolkit_console as JTKExternConsole
import jarbin_toolkit_error as JTKExternError

import jardiscordengine.interns.final_classes as FinalClasses
import jardiscordengine.interns.high_classes as HighClasses
import jardiscordengine.interns.low_classes as LowClasses
from jardiscordengine.interns.base_classe import JDEInternBaseClass
import jardiscordengine.interns.decorators as Decorators

__all__ = [
    "JDEInternBaseClass",
    "Decorators",
    "FinalClasses",
    "HighClasses",
    "LowClasses",
    "DiscordExtern",
    "JTKExternConsole",
    "JTKExternError",
]
