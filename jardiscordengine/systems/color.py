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

from typing import final as _final

from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns.base_classe import JDEInternBaseClass as _JDEInternBaseClass
from jardiscordengine.interns.decorators import documentation as _documentation

@_documentation
@_final
class JDEColor(_JDEInternBaseClass):

    __recursive__ = False

    fields = ("red", "green", "blue", "alpha")

    def __init__(self, r = 0, g = 0, b = 0, a = 255):
        super().__init__()

        self._color = [r, g, b, a]

        for c in self._color:
            if not (0 <= c <= 255):
                raise _JTKExternError.JErrorValue("Invalid color, every channels must be between 0 and 255.")

    @property
    def r(self):
        return self._color[0]

    @r.setter
    def r(self, r):
        self._color[0] = r

    @property
    def g(self):
        return self._color[1]

    @g.setter
    def g(self, g):
        self._color[1] = g

    @property
    def b(self):
        return self._color[2]

    @b.setter
    def b(self, b):
        self._color[2] = b

    @property
    def a(self):
        return self._color[3]

    @a.setter
    def a(self, a):
        self._color[3] = a

    @property
    def rgb(self):
        return tuple(self._color[:3])

    @rgb.setter
    def rgb(self, rgb):
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

    @property
    def rgba(self):
        return tuple(self._color)

    @rgba.setter
    def rgba(self, rgba):
        self.r = rgba[0]
        self.g = rgba[1]
        self.b = rgba[2]
        self.a = rgba[3]

    def __iter__(self):
        return iter(self._color)

    def __getitem__(self, index):
        return self._color[index]

    def __repr__(self):
        fields = (
            f"{name}={value}"
            for name, value in zip(self.fields, self._color)
        )

        return f"<{self.__class__.__name__}({', '.join(fields)})>"
