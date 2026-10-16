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

from enum import IntEnum
from typing import Iterator

from jardiscordengine.interns.base_classe import JDEInternBaseClass

class JDECompatibility(IntEnum):
    OK: int
    WARNING: int
    ERROR: int

class JDEVersion(JDEInternBaseClass):

    fields: list[str]

    def __init__(self, major: int, minor: int, patch: int):
        """
            JDEVersion

            Parameters:
                major (int): Major version
                minor (int): Minor version
                patch (int): Patch version
        """
        ...
    def __str__(self) -> str:
        """
            Get string of the version

            Returns:
                str: String of the version
        """
        ...
    def __iter__(self) -> Iterator[int]:
        """
            Iterate over the version

            Returns:
                Iterator[int]: Iterator of the version
        """
        ...
    def __getitem__(self, index: int | slice) -> list[int]:
        """
            Get a specific version or version slice

            Returns:
                list[int]: Version or version slice
        """
        ...
    @property
    def major(self) -> int:
        """
            Get major version

            Returns:
                int: Major version
        """
        ...
    @property
    def minor(self) -> int:
        """
            Get minor version

            Returns:
                int: Minor version
        """
        ...
    @property
    def patch(self) -> int:
        """
            Get patch version

            Returns:
                int: Patch version
        """
        ...
    def compatibility(self, other: JDEVersion) -> int:
        """
            Check backward compatibility
            
            Parameters:
                other (JEVersion): JEVersion
            
            Returns:
                
        """
        ...
