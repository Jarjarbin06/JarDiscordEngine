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

from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import field as _field
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.low_classes import (
    JDEInternField as _JDEInternField,
)


@_documented
class JDEInternFieldID(_JDEInternField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    id = _field(int, required=True, read_only=True, doc="Discord ID")

    def __new__(cls, id, _jde_key = None, _jde_warn = None):
        return _JDEInternField.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else id,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, id):
        _JDEInternField.__init__(self)

        self.id = id

@_documented
class JDEInternFieldUsername(_JDEInternField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    username = _field(str, required=True, doc="Username")

    def __new__(cls, username, _jde_key = None, _jde_warn = None):
        return _JDEInternField.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, username):
        _JDEInternField.__init__(self)

        self.username = username

@_documented
class JDEInternFieldName(_JDEInternField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    name = _field(str, required=True, read_only=True, doc="Name")

    def __new__(cls, name, _jde_key = None, _jde_warn = None):
        return _JDEInternField.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else name,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, name):
        _JDEInternField.__init__(self)

        self.name = name

@_documented
class JDEInternFieldURL(_JDEInternField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    url = _field(str, required=True, read_only=True, doc="URL")

    def __new__(cls, url, _jde_key = None, _jde_warn = None):
        return _JDEInternField.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, url):
        _assert_is_instance(url, str, "URL must be str")

        _JDEInternField.__init__(self)

        self.url = url

@_documented
class JDEInternFieldDiscord(_JDEInternField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    discord = _field(object, required=True, read_only=True, doc="Discord object", setter_check=lambda instance: getattr(instance, "_jde_initializing", False))

    def __new__(cls, _jde_key = None, _jde_warn = None):
        return _JDEInternField.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, discord):
        _JDEInternField.__init__(self)

        self._jde_initializing = True
        try:
            self.discord = discord
        finally:
            self._jde_initializing = False
