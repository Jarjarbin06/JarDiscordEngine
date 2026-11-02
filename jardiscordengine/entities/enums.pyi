from collections.abc import Sequence
from enum import IntEnum, StrEnum
from typing import final

@final
class JDEActivityType(IntEnum):
    """
    Discord activity type.

    Attributes:
        UNKNOWN (int): Unknown activity.
        PLAYING (int): Playing (video games).
        STREAMING (int): Streaming (twitch/youtube/etc...).
        LISTENING (int): Listening to music (spotify/deezer/youtube music/etc...).
        WATCHING (int): Watching content (video/movie/series/etc...).
        CUSTOM (int): Custom activity.
        COMPETING (int): Competing (video game).
    """

    UNKNOWN: int
    PLAYING: int
    STREAMING: int
    LISTENING: int
    WATCHING: int
    CUSTOM: int
    COMPETING: int

@final
class JDEStatus(StrEnum):
    """
    Discord user status.

    Attributes:
        ONLINE (str): Online.
        OFFLINE (str): Offline.
        IDLE (str): Idle.
        DND (str): Do not disturb.
        DO_NOT_DISTURB (str): Do not disturb (DND alias).
        INVISIBLE (str): Invisible.
        STREAMING (str): Streaming.
    """

    ONLINE: str
    OFFLINE: str
    IDLE: str
    DND: str
    DO_NOT_DISTURB: str
    INVISIBLE: str
    STREAMING: str

__all__: Sequence[str] = [
    "JDEActivityType",
    "JDEStatus",
]
