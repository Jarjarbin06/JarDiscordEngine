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

from jardiscordengine.interns.decorators import documentation as _documentation
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.low_classes import (
    JDEInternEntityField as _JDEInternEntityField,
)


@_documentation
class JDEInternEntityFieldID(_JDEInternEntityField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, id, _jde_key = None, _jde_warn = None):
        return _JDEInternEntityField.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else id,
            _jde_warn=_jde_warn,
        )

    def __init__(self, id):
        _assert_is_instance(id, int, "ID must be int")

        _JDEInternEntityField.__init__(self)

        self._id = id

    @property
    def id(self):
        return self._id

@_documentation
class JDEInternEntityFieldUsername(_JDEInternEntityField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, username, _jde_key = None, _jde_warn = None):
        return _JDEInternEntityField.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn,
        )

    def __init__(self, username):
        _assert_is_instance(username, str, "USERNAME must be str")

        _JDEInternEntityField.__init__(self)

        self._username = username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

@_documentation
class JDEInternEntityFieldName(_JDEInternEntityField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, name, _jde_key = None, _jde_warn = None):
        return _JDEInternEntityField.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else name,
            _jde_warn=_jde_warn,
        )

    def __init__(self, name):
        _assert_is_instance(name, str, "NAME must be str")

        _JDEInternEntityField.__init__(self)

        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

@_documentation
class JDEInternEntityFieldURL(_JDEInternEntityField):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, url, _jde_key = None, _jde_warn = None):
        return _JDEInternEntityField.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn,
        )

    def __init__(self, url):
        _assert_is_instance(url, str, "URL must be str")

        _JDEInternEntityField.__init__(self)

        self._url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
