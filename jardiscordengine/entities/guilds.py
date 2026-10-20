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

from jardiscordengine.interns.enums import JDEInternInstancePolicy as _JDEInternInstancePolicy
from jardiscordengine.interns.decorators import documentation as _documentation
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity
from jardiscordengine.interns.high_classes import (
    JDEInternEntityFieldID as _JDEInternEntityFieldID,
    JDEInternEntityFieldName as _JDEInternEntityFieldName
)

@_documentation
class JDEEntityGuild(_JDEInternEntity, _JDEInternEntityFieldID, _JDEInternEntityFieldName):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, id, name, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else id,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, id, name):
        _JDEInternEntity.__init__(self)
        _JDEInternEntityFieldID.__init__(self, id)
        _JDEInternEntityFieldName.__init__(self, name)
