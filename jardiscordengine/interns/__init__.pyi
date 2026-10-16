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

"""
JarDiscordEngine internal module.

Provides internal engine classes, configurations, decorators,
and external integrations required by JarDiscordEngine.

Warning:
    This module is intended for engine development and advanced usage.
    Users should avoid directly modifying or relying on its internals.
"""

from __future__ import annotations

# Public API exports
from .base_classe import JDEInternBaseClass
from . import decorators as Decorators
from . import final_classes as FinalClasses
from . import high_classes as HighClasses
from . import low_classes as LowClasses

# Submodules
import jarbin_toolkit_console as JTKExternConsole
import jarbin_toolkit_error as JTKExternError
import discord as DiscordExtern


__all__: list[str] = [
    "JDEInternBaseClass",
    "Decorators",
    "FinalClasses",
    "HighClasses",
    "LowClasses",
    "JTKExternConsole",
    "JTKExternError",
    "DiscordExtern",
]
