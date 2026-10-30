"""
JarDiscordEngine - Commands

Command creation and handling.
"""

from collections.abc import Sequence

from .command_manager import JDECommandManager as JDECommandManager
from .decorators import (
    bot_has_permissions as bot_has_permissions,
)
from .decorators import (
    checks as checks,
)
from .decorators import (
    command as command,
)
from .decorators import (
    cooldown as cooldown,
)
from .decorators import (
    guild_only as guild_only,
)
from .decorators import (
    has_permissions as has_permissions,
)
from .decorators import (
    is_owner as is_owner,
)
from .decorators import (
    option as option,
)

__all__: Sequence[str] = [
    "JDECommandManager",
    "bot_has_permissions",
    "checks",
    "command",
    "cooldown",
    "guild_only",
    "has_permissions",
    "is_owner",
    "option"
]
