"""
JarDiscordEngine - Bots

Bot creation and bot-related handling.
"""

from collections.abc import Sequence

from .bot import JDEBot as JDEBot
from .guild_manager import JDEGuildManager as JDEGuildManager

__all_: Sequence[str] = [
    "JDEBot",
    "JDEGuildManager"
]
