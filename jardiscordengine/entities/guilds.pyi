from collections.abc import Sequence

from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldID,
    JDEInternFieldName,
)
from jardiscordengine.interns.low_classes import JDEInternEntity

class JDEEntityGuild(
    JDEInternEntity,
    JDEInternFieldID,
    JDEInternFieldName,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Guild entity."""

    def __init__(
        self,
        id: int,
        name: str
    ) -> None:
        """
        Initialize a guild.

        Args:
            id (int): Discord ID.
            name (str): Name.
        """

__all__: Sequence[str] = [
    "JDEEntityGuild",
]
