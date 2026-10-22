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


def assert_is_instance(obj, cls, msg=None):
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

def error(err):
    if isinstance(err, _JTKExternError.BaseJError):
        err = _JTKExternError.BaseJError(
            err.message.splitlines()[-1].replace("→", "").replace(":", " →").strip(),
            error="Error",
            format=_JTKExternError.FormatType.COMPACT
        )

    title, message = str(err).split(":")

    _JTKExternConsole.print(
        _JTKExternConsole.Text(f" JDE - {title.strip()} ").f_color_error(background=True).f_color_black(),
        _JTKExternConsole.Text(" : " + message.strip().removeprefix("'").removesuffix("'")).f_color_error(),
        stream=sys.stderr,
        separator="",
    )

def warning(err):
    if isinstance(err, _JTKExternError.BaseJError):
        err = _JTKExternError.BaseJError(
            err.message.splitlines()[-1].replace("→", "").replace(":", " →").strip(),
            error="Warning",
            format=_JTKExternError.FormatType.COMPACT
        )

    title, message = str(err).split(":")

    _JTKExternConsole.print(
        _JTKExternConsole.Text(f" JDE - {title.strip()} ").f_color_warning(background=True).f_color_black(),
        _JTKExternConsole.Text(" : " + message.strip().removeprefix("'").removesuffix("'")).f_color_warning(),
        stream=sys.stderr,
        separator="",
    )

def version(config, section, key):
    from jardiscordengine.interns.config import get as _get
    from jardiscordengine.systems.version import JDEVersion as _JDEVersion

    return _JDEVersion(*[int(v) for v in _get(config, section, key).split(".")])

def enabled(config, section, setting = "enabled"):
    from jardiscordengine.interns.config import get as _get

    return _get(config, section, setting, bool, False)
