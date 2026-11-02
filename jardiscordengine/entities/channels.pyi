from collections.abc import Sequence

from jardiscordengine.entities.guilds import JDEEntityGuild
from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldDiscord,
    JDEInternFieldID,
    JDEInternFieldName,
)
from jardiscordengine.interns.low_classes import JDEInternEntity

class JDEEntityChannel(
    JDEInternEntity,
    JDEInternFieldID,
    JDEInternFieldName,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Channel entity."""

    def __init__(
        self,
        id: int,
        name: str
    ) -> None:
        """
        Initialize a channel.

        Args:
            id (int): Discord ID.
            name (str): Name.
        """

class JDEEntityGuildChannel(
    JDEEntityChannel,
    JDEInternFieldDiscord,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Guild channel entity."""

    guild: JDEEntityChannel

    def __init__(
        self,
        channel: JDEEntityChannel,
        guild: JDEEntityGuild
    ) -> None:
        """
        Initialize a guild channel.

        Args:
            channel (JDEEntityChannel): Channel entity.
            guild (JDEEntityGuild): Guild entity.
        """

    async def send(
        self,
        content: str
    ) -> None:
        """
        Send a simple message to the current channel.

        Args:
            content (str): Message.
        """

class JDEEntityTextChannel(
    JDEEntityGuildChannel,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Text channel entity."""

class JDEEntityVoiceChannel(
    JDEEntityGuildChannel,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Voice channel entity."""

class JDEEntityStageChannel(
    JDEEntityGuildChannel,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Stage channel entity."""

class JDEEntityForumChannel(
    JDEEntityGuildChannel,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Forum channel entity."""

class JDEEntityAnnouncementChannel(
    JDEEntityGuildChannel,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Announcement channel entity."""

__all__: Sequence[str] = [
    "JDEEntityAnnouncementChannel",
    "JDEEntityChannel",
    "JDEEntityForumChannel",
    "JDEEntityGuildChannel",
    "JDEEntityStageChannel",
    "JDEEntityTextChannel",
    "JDEEntityVoiceChannel",
]
