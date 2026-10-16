# =============================================================================
# JarDiscordEngine - Python Discord Bot Engine (discord.py-based)
# =============================================================================
#
# JarDiscordEngine is a lightweight bot framework built on top of discord.py
# that simplifies Discord bot development while providing higher-level
# abstractions for command management, event handling, and extensibility.
#
# =============================================================================
# Version: jardiscordengine-v1
# Author: Jarjarbin Studio
# Licence: GPL v3
# =============================================================================
#
# This engine is inspired by discord.py, modern bot framework design patterns,
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
# This is NOT discord.py itself.
# It is a custom abstraction layer built on top of discord.py.
#
# =============================================================================

"""
JarDiscordEngine core module.

Provides the main interface of the engine, including bot management,
commands, entities, events, extensions, and engine-wide utilities.
"""

from __future__ import annotations

from typing import Any, Callable

# Public API
from . import bots as Bots
from . import commands as Commands
from . import entities as Entities
from . import events as Events
from . import extensions as Extensions
from . import interns as Interns
from . import services as Services
from . import systems as Systems

# Constants
from .constants import *

__author__: str
__email__: str
__version__: str
__config_version__: str
__license__: str

__all__: list[str] = [
    ## Special ##
    "__author__",
    "__email__",
    "__version__",
    "__license__",
    ## Imports ##
    'Bots',
    'Commands',
    'Entities',
    'Events',
    'Extensions',
    'Interns',
    'Services',
    'Systems',
    ## Constants ##
    # Versions #
    'JDEVersion_JarEngine',
    'JDEVersion_Python',
    # Booleans #
    'JDEFalse',
    'JDETrue',
]
