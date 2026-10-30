"""
JarDiscordEngine - Terminals

Terminal creation, command creation and handling.
"""

from .decorator import (
    terminal_command as terminal_command,
)
from .terminal import (
    JDETerminal as JDETerminal,
)
from .terminal import (
    JDETerminalRestart as JDETerminalRestart,
)

__all__ = [
    "JDETerminal",
    "JDETerminalRestart",
    "terminal_command",
]
