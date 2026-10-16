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

from typing import Iterator

from jardiscordengine.interns.base_classe import JDEInternBaseClass

class JDEColor(JDEInternBaseClass):

    fields: list[str]

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 255):
        """
        JEColor

            Parameters:
                r (int) = 0: Red channel (0 - 255)
                g (int) = 0: Green channel (0 - 255)
                b (int) = 0: Blue channel (0 - 255)
                a (int) = 255: Alpha channel (opacity)(0 - 255)
        """
        ...
    @property
    def r(self) -> int:
        """
            Get the red channel value

            Returns:
                int: Red channel
        """
        ...
    @r.setter
    def r(self, r: int):
        """
            Set the red channel value

            Parameters:
                r (int): Red channel value
        """
        ...
    @property
    def g(self) -> int:
        """
            Get the green channel value

            Returns:
                int: Green channel
        """
        ...
    @g.setter
    def g(self, g: int):
        """
            Set the green channel value

            Parameters:
                g (int): Green channel value
        """
        ...
    @property
    def b(self) -> int:
        """
            Get the blue channel value

            Returns:
                int: Blue channel
        """
        ...
    @b.setter
    def b(self, b: int):
        """
            Set the blue channel value

            Parameters:
                b (int): Blue channel value
        """
        ...
    @property
    def a(self) -> int:
        """
            Get the alpha channel value

            Returns:
                int: Alpha channel
        """
        ...
    @a.setter
    def a(self, a: int):
        """
            Set the alpha channel value

            Parameters:
                a (int): Alpha channel value
        """
        ...
    @property
    def rgb(self) -> tuple[int, int, int]:
        """
            Get the RGB value as a tuple

            Returns:
                tuple[int, int, int]: RGB value
        """
        ...
    @rgb.setter
    def rgb(self, rgb: tuple[int, int, int]):
        """
            Set the RGBA value as a tuple

            Parameters:
                rgb (tuple[int, int, int]): RGB value
        """
        ...
    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """
            Get the RGBA value as a tuple

            Returns:
                tuple[int, int, int, int]: RGBA value
        """
        ...
    @rgba.setter
    def rgba(self, rgba: tuple[int, int, int, int]):
        """
            Set the RGBA value as a tuple

            Parameters:
                rgba (tuple[int, int, int, int]): RGBA value
        """
        ...
    def __iter__(self) -> Iterator[float]:
        """
            Iterate over the channels

            Returns:
                Iterator[float]: Color iterator
        """
        ...
    def __getitem__(self, index: int | slice) -> list[int]:
        """
            Get a specific version or version slice

            Returns:
                list[int]: Version or version slice
        """
        ...
    def __repr__(self) -> str:
        """
            Get the representation of the channels

            Returns:
                str: Representation of the channels
        """
        ...
