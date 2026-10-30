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

import sys

from jardiscordengine.interns import JTKExternConsole as _JTKExternConsole
from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns.decorators import _ENTITY_REGISTRY, _ENTITY_REGISTRY_LOCK
from jardiscordengine.interns.decorators import requires_init as _requires_init

HAS_CRITICAL = False

def assert_is_instance(obj, cls, msg = None):
    if not isinstance(obj, cls):
        raise _JTKExternError.JErrorType(
            "Invalid type" if msg is None else msg,
        )

def deprecated(func, new_func, version = None):

    def callable_path(func):
        return f"{_JTKExternConsole.Text(f'{func.__qualname__}(...)').f_style_bold()} in {_JTKExternConsole.Text(func.__module__).f_style_bold()}"

    message = (
        f"Function {callable_path(func)} is deprecated"
        f"\nUse {callable_path(new_func)} instead."
    )
    if version:
        message += f"\n  → deprecated since {version}"

    _JTKExternConsole.print(
        _JTKExternConsole.Text(" JDE - Deprecated ").f_color_white(background=True).f_color_black(),
        _JTKExternConsole.Text(" :\n").f_color_white(),
        _JTKExternConsole.Text(message).f_color_white().f_layout_indent(1),
        stream=sys.stderr,
        separator="",
    )

def critical(err, show = True):
    from jardiscordengine.interns.log import log as _log

    global HAS_CRITICAL

    HAS_CRITICAL = True

    if isinstance(err, _JTKExternError.BaseJError):
        err = _JTKExternError.BaseJError(
            err.message.splitlines()[-1].replace("→", "").replace(":", " →").strip(),
            error="Critical",
            format=_JTKExternError.FormatType.COMPACT  # pyright: ignore[reportArgumentType]
        )
    else:
        err = _JTKExternError.BaseJError(
            str(err).replace(":", " →").strip(),
            error="Critical",
            format=_JTKExternError.FormatType.COMPACT  # pyright: ignore[reportArgumentType]
        )

    if show:
        title, message = str(err).split(":")

        _JTKExternConsole.print(
            _JTKExternConsole.Text(f" JDE - {title.strip()} ").f_color_error(background=True).f_color_black(),
            _JTKExternConsole.Text(" : " + message.strip().removeprefix("'").removesuffix("'")).f_color_error(background=True).f_color_black(),
            stream=sys.stderr,
            separator="",
        )

    _log("CRIT", "ENGINE", err.message)

def error(err, show = True):
    from jardiscordengine.interns.log import log as _log

    if isinstance(err, _JTKExternError.BaseJError):
        err = _JTKExternError.BaseJError(
            err.message.splitlines()[-1].replace("→", "").replace(":", " →").strip(),
            error="Error",
            format=_JTKExternError.FormatType.COMPACT  # pyright: ignore[reportArgumentType]
        )
    else:
        err = _JTKExternError.BaseJError(
            str(err).replace(":", " →").strip(),
            error="Error",
            format=_JTKExternError.FormatType.COMPACT  # pyright: ignore[reportArgumentType]
        )

    if show:
        title, message = str(err).split(":")

        _JTKExternConsole.print(
            _JTKExternConsole.Text(f" JDE - {title.strip()} ").f_color_error(background=True).f_color_black(),
            _JTKExternConsole.Text(" : " + message.strip().removeprefix("'").removesuffix("'")).f_color_error(),
            stream=sys.stderr,
            separator="",
        )

    _log("ERROR", "ENGINE", err.message)

def warning(err, show = True):
    from jardiscordengine.interns.log import log as _log

    if isinstance(err, _JTKExternError.BaseJError):
        err = _JTKExternError.BaseJError(
            err.message.splitlines()[-1].replace("→", "").replace(":", " →").strip(),
            error="Warning",
            format=_JTKExternError.FormatType.COMPACT  # pyright: ignore[reportArgumentType]
        )

    if show:
        title, message = str(err).split(":")

        _JTKExternConsole.print(
            _JTKExternConsole.Text(f" JDE - {title.strip()} ").f_color_warning(background=True).f_color_black(),
            _JTKExternConsole.Text(" : " + message.strip().removeprefix("'").removesuffix("'")).f_color_warning(),
            stream=sys.stderr,
            separator="",
        )

    _log("WARN", "ENGINE", err.message)

@_requires_init
def version(config, section, key):
    from jardiscordengine.interns.config import get as _get
    from jardiscordengine.systems.version import JDEVersion as _JDEVersion

    return _JDEVersion(*[int(v) for v in _get(config, section, key).split(".")])

@_requires_init
def enabled(config, section, setting = "enabled"):
    from jardiscordengine.interns.config import get as _get

    return _get(config, section, setting, bool, False)

def get_registered_entities(category = None):
    with _ENTITY_REGISTRY_LOCK:
        if category is None:
            return dict(_ENTITY_REGISTRY)

        return {
            name: entity
            for (entity_category, name), entity in _ENTITY_REGISTRY.items()
            if entity_category == category
        }

def get_registered_entity(name, *, category = "entity"):
    with _ENTITY_REGISTRY_LOCK:
        try:
            return _ENTITY_REGISTRY[(category, name)]
        except KeyError:
            raise LookupError(
                f"No entity named {name!r} is registered "
                f"in category {category!r}"
            ) from None

__all__ = [
    "assert_is_instance",
    "critical",
    "deprecated",
    "enabled",
    "error",
    "get_registered_entities",
    "get_registered_entity",
    "version",
    "warning",
]
