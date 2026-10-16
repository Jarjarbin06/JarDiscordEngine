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

from __future__ import annotations

from typing import Any

from jardiscordengine.interns.base_classe import JDEInternBaseClass

class JDEBool(JDEInternBaseClass):
    def __init__(self, value: Any):
        """
            JDEBool

            Parameters:
                value (Any): Value to be represented
        """
        ...
    def __bool__(self) -> bool:
        """
            Get the actual intern boolean (used in conditions)

            Returns:
                bool: Internal boolean
        """
        ...
    def __int__(self) -> int:
        """
            Get int representation of the boolean

            Returns:
                int: Int
        """
        ...
    def __str__(self) -> str:
        """
            Get the string of the boolean

            Returns:
                str: String
        """
        ...
    def __repr__(self) -> str:
        """
            Get the string representation of the boolean

            Returns:
                str: String representation
        """
        ...
    def __call__(self) -> JDEBool:
        """
            Revers the boolean (False <-> True)

            Returns:
                JDEBool: Reversed boolean
        """
        ...
    def __or__(self, other):
        """
            Run the OR logic gate

            Returns:
                JDEBool: OR result
        """
        ...
    def __and__(self, other):
        """
            Run the AND logic gate

            Returns:
                JDEBool: AND result
        """
        ...
    @property
    def b(self) -> bool:
        """
            Get the actual intern boolean (used for dump and debug)

            Returns:
                bool: Internal boolean
        """
        ...
