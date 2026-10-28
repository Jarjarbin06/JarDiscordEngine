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

import re
from typing import final as _final

from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns import JTKExternLog as _JTKExternLog
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass as _JDEInternBaseClass,
)
from jardiscordengine.interns.config import get as _get
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import requires_init as _requires_init
from jardiscordengine.interns.enums import JDEInternInstancePolicy

current_logs = {
    "base": None,
    "crash": None
}
_log_levels = ["DEBUG", "INFO", "NOTICE", "WARN", "ERROR", "CRIT"]
_ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


@_documented
@_final
class JDEInternLog(_JTKExternLog.Log, _JDEInternBaseClass):

    __instance_policy__ = JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    project_path = None
    log_path = None

    @_requires_init
    def __new__(cls, name, _session, _jde_key=None, _jde_warn=None, **kwargs):
        return _JDEInternBaseClass.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else name,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    @_requires_init
    def __init__(self, name, _session):
        if not JDEInternLog.project_path or not JDEInternLog.log_path:
            raise _JTKExternError.JErrorRuntime(
                "JarDiscordEngine.init(path) must be called first"
            )

        _JTKExternLog.Log.__init__(
            self,
            JDEInternLog.log_path,
            name,
            type=_JTKExternLog.LogType.JAR_LOG,
            metadata={
                "application": _get('project', 'PROJECT', 'name', str, "Unnamed project"),  # pyright: ignore[reportArgumentType]
                "description": _get('project', 'PROJECT', 'description', str, "No description"),  # pyright: ignore[reportArgumentType]
                "version": _get('project', 'PROJECT', 'version', str, "0.0.0"),  # pyright: ignore[reportArgumentType]
            },
            run_id=_session,
        )
        _JDEInternBaseClass.__init__(self)

        current_logs["base"] = self  # pyright: ignore[reportArgumentType]

def _clean_text(text):
    if isinstance(text, _JTKExternError.BaseJError):
        return f"{text.error}{''.join([f'\n    {line}' for line in text.message.removeprefix("\n").split("\n")])}"
    text.strip().replace("  ", " ")
    if "\033" in text:
        return _ansi_escape.sub("", text)
    return text

@_requires_init
def log(status, title, description, jdeid=None, *values):
    if current_logs["base"] is None:
        return

    status = status.upper()
    title = title.upper()
    description = _clean_text(description)

    _description = description.lower()

    if jdeid is not None:
        description += f" (JDEID:{jdeid})"

    if values:
        description += f" (VALUES:{', '.join(map(repr, values))})"

    current_logs["base"].log(
        _JTKExternLog.LogLevel(status),
        description,
        scope=title,
    )

@_requires_init
def comment(comment):
    if current_logs["base"] is not None:
        current_logs["base"].comment(_clean_text(comment))

@_requires_init
def save():
    if current_logs["base"] is None:
        return

    current_logs["base"].flush()

@_requires_init
def close():
    from jardiscordengine.interns.helpers import HAS_CRITICAL

    if current_logs["base"] is None:
        return

    current_log = current_logs["base"]

    current_log.flush()
    current_log.close(result="FAIL" if HAS_CRITICAL else "SUCCESS")

    current_logs["base"] = None

__all__ = [
    "JDEInternLog",
    "close",
    "comment",
    "log",
    "save",
]
