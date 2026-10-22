import re
from typing import Any, Literal, final

from jarbin_toolkit_log import (
    Log as JTKExternLog,
)
from jarbin_toolkit_log import (
    LogLevel,
)
from jarbin_toolkit_log import (
    LogType,
)

from jardiscordengine.interns import JTKExternError
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass,
)
from jardiscordengine.interns.config import get
from jardiscordengine.interns.decorators import documentation
from jardiscordengine.interns.enums import JDEInternInstancePolicy

current_logs: dict[str, JDEInternLog]

@documentation
@final
class JDEInternLog(
    JTKExternLog,
    JDEInternBaseClass[
        Literal[JDEInternInstancePolicy.UNIQUE],
        Literal[0],
        Literal[False],
    ]
):

    project_path: str | None
    log_path: str | None

    def __init__(
        self,
        name: str,
    ) -> None:
        """
        Initialize a log file.

        Args:
            name (str): File name
        """

def log(
    status: Literal["DEBUG", "INFO", "NOTICE", "WARN", "ERROR", "CRIT"],
    title: str,
    description: str,
    jdeid: str | None = None,
    *values: Any
) -> None:
    """
    Create a new log entry.

    Args:
        status (Literal["DEBUG", "INFO", "NOTICE", "WARN", "ERROR", "CRIT"]): Log status.
        title (str): Log title.
        description (str): Log description.
        jdeid (str | None): Append jdeid to the entry.
        *values (Any): Append values to the entry.
    """

def comment(
    comment: str
) -> None:
    """
    Create a new comment entry.

    Args:
        comment (str): Comment entry.
    """

def save(
) -> None:
    """Save the pending entries."""

def close():
    """Save and close the log file."""
