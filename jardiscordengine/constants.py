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

from sys import version_info as _python_version

from jardiscordengine import __version__ as _jarengine_version
from jardiscordengine.systems.bool import JDEBool as _JDEBool
from jardiscordengine.systems.version import JDEVersion as _JDEVersion

# Versions #
JDEVersion_JarEngine = _JDEVersion(*[int(v) for v in _jarengine_version.split('.')])
JDEVersion_Python = _JDEVersion(*_python_version[0:3])

# Booleans #
JDEFalse = _JDEBool(0)
JDETrue = _JDEBool(1)

__all__ = [  # noqa: RUF022
    # Versions #
    'JDEVersion_JarEngine',
    'JDEVersion_Python',
    # Booleans #
    'JDEFalse',
    'JDETrue',
]
