"""
JarDiscordEngine - Terminals

Terminal creation, command creation and handling.
"""

from collections.abc import Sequence

from .decorator import (
    terminal_command,
)
from .terminal import (
    JDETerminal,
    JDETerminalRestart,
)

__all__: Sequence[str] = [
    "JDETerminal",
    "JDETerminalRestart",
    "terminal_command",
]
