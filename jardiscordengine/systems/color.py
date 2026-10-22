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

from typing import final as _final

from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass as _JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import documentation as _documentation
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance


@_documentation
@_final
class JDEColor(_JDEInternBaseClass):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    _fields = ("red", "green", "blue", "alpha")

    def __new__(cls, r, g, b, a, _jde_key = None, _jde_warn = None):
        return _JDEInternBaseClass.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else False,
        )

    def __init__(self, r = 0, g = 0, b = 0, a = 255):
        _assert_is_instance(r, int, "R must be int")
        _assert_is_instance(g, int, "G must be int")
        _assert_is_instance(b, int, "B must be int")
        _assert_is_instance(a, int, "A must be int")

        _JDEInternBaseClass.__init__(self)

        self._color = [r, g, b, a]

        for c in self._color:
            if not (0 <= c <= 255):
                raise _JTKExternError.JErrorValue("Invalid color, every channels must be between 0 and 255.")

    @property
    def r(self):
        return self._color[0]

    @r.setter
    def r(self, r):
        _assert_is_instance(r, int, "R must be int")

        self._color[0] = r

    @property
    def g(self):
        return self._color[1]

    @g.setter
    def g(self, g):
        _assert_is_instance(g, int, "G must be int")

        self._color[1] = g

    @property
    def b(self):
        return self._color[2]

    @b.setter
    def b(self, b):
        _assert_is_instance(b, int, "B must be int")

        self._color[2] = b

    @property
    def a(self):
        return self._color[3]

    @a.setter
    def a(self, a):
        _assert_is_instance(a, int, "A must be int")

        self._color[3] = a

    @property
    def rgb(self):
        return tuple(self._color[:3])

    @rgb.setter
    def rgb(self, rgb):
        _assert_is_instance(rgb, tuple | list, "RGB must be tuple or list")

        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

    @property
    def rgba(self):
        return tuple(self._color)

    @rgba.setter
    def rgba(self, rgba):
        _assert_is_instance(rgba, tuple | list, "RGBA must be tuple or list")

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
            for name, value in zip(self._fields, self._color)
        )

        return f"<{self.__class__.__name__}({', '.join(fields)})>"

__all__ = [
    "JDEColor",
]
