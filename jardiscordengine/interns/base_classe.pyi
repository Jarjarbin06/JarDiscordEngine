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

from typing import Optional

class JDEInternBaseClass:
    __instance_policy__: str            #How the class handles instances (normal/flyweight/singleton). Default: normal
    __instance_limit__: Optional[int]   #How many instances are allowed (None/inf.). Default: None
    __recursive__: bool                 #Is the class pointing to itself (directly or indirectly)(used by dump and debug). Default: True

    def __init__(self):
        """
            JDEInternBaseClass
        """
        ...
    @property
    def jeid(self) -> str:
        """
            Get the JarDiscordEngine ID (JDEID) of the object

            Returns:
                str: JarDiscordEngine ID
        """
        ...
    @jeid.setter
    def jeid(self, /) -> str:
        """
            Set the JarDiscordEngine ID (JDEID) of the object will immediately raise an error
        """
        ...
    def __str__(self) -> str:
        """
            Get the string version of the class

            Returns:
                str: String version of the class
        """
        ...
    def __repr__(self) -> str:
        """
            Get the string representation of the class

            Returns:
                str: String representation of the class
        """
        ...
    def to_dict(self) -> dict:
        """
            Get the dictionary representation of the class and its public variables

            Returns:
                dict: Dictionary of the class
        """
        ...
    def debug(self, *, is_colored: bool = False, max_depth: int = -1, branched_recursive: bool = False, show_root: bool = True) -> str:
        """
            Show full, detailed debug of the class
            
            Parameters:
                is_colored (bool) = False: Show color coded debug
                max_depth (int) = -1: Maximum depth of the recursion (-1 for infinite)
                branched_recursive (bool) = False: Block recursion (when we meet the same object a 2nd time) per branch or global
                show_root (bool) = False: Show root of the recursion
            
            Returns:
                str: Debug string
        """
        ...
    def dump(self):
        """
            Show simple debug of the class

            Returns:
                str: Debug string
        """
        ...
