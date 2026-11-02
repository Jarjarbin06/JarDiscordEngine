from collections.abc import Sequence

from jardiscordengine.entities.guilds import JDEEntityGuild
from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldName,
    JDEInternFieldURL,
)
from jardiscordengine.interns.low_classes import JDEInternEntity

class JDEEntityEmoji(
    JDEInternEntity,
    JDEInternFieldName,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """
    Emoji entity.

    Attributes:
        emoji (str): Emoji.
        guild (JDEEntityGuild | None): Guild the emoji is from (if not base discord emoji).
        animated (bool): Is the emoji animated
    """

    emoji: str
    guild: JDEEntityGuild | None = None
    animated: bool

    def __init__(
        self,
        emoji: str,
        name: str,
        guild: JDEEntityGuild | None = None,
        animated: bool = False
    ) -> None:
        """
        Initialize an emoji.

        Args:
            emoji (str): Emoji.
            name (str): Name.
            guild (JDEEntityGuild | None): Guild emoji.
            animated (bool): Is animated.
        """

class JDEEntityCustomEmoji(
    JDEEntityEmoji,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Custom emoji entity."""

class JDEEntityImage(
    JDEInternEntity,
    JDEInternFieldURL,
    JDEInternFieldName,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Image entity."""

    def __init__(
        self,
        url: str,
        name: str | None = None
    ) -> None:
        """
        Initialize an image from URL.

        Args:
            url (str): Image URL source.
            name (str | None): Image name (URL if none).
        """

class JDEEntityAvatar(
    JDEEntityImage,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Avatar entity."""

class JDEEntityGuildIcon(
    JDEEntityImage,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Guild icon entity."""

class JDEEntityBanner(
    JDEEntityImage,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Banner entity."""

class JDEEntitySticker(
    JDEEntityImage,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Sticker entity."""

__all__: Sequence[str] = [
    "JDEEntityAvatar",
    "JDEEntityBanner",
    "JDEEntityCustomEmoji",
    "JDEEntityEmoji",
    "JDEEntityGuildIcon",
    "JDEEntityImage",
    "JDEEntitySticker",
]
