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

class JDEEntityCategory(
    JDEInternEntity,
    JDEInternFieldID,
    JDEInternFieldName,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Category entity."""

    def __init__(
        self,
        id: int,
        name: str
    ) -> None:
        """
        Initialize a category.

        Args:
            id (int): Description.
            name (str): Description.
        """

class JDEEntityGuildCategory(
    JDEEntityCategory,
    JDEInternFieldDiscord,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Guild category entity."""

    guild: JDEEntityGuild

    def __init__(
        self,
        category: JDEEntityGuild,
        guild: JDEEntityGuild
    ) -> None:
        """
        Initialize a guild category.

        Args:
            category (JDEEntityGuild): Category entity.
            guild (JDEEntityGuild): Guild entity.
        """

__all__: Sequence[str] = [
    "JDEEntityCategory",
    "JDEEntityGuildCategory",
]
