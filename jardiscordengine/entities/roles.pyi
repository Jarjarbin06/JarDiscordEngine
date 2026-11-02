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

class JDEEntityRole(
    JDEInternEntity,
    JDEInternFieldID,
    JDEInternFieldName,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """Role entity."""

    def __init__(
        self,
        id: int,
        name: str
    ) -> None:
        """
        Initialize role.

        Args:
            id (int): Discord ID.
            name (str): Name.
        """

__all__: Sequence[str] = [
    "JDEEntityRole",
]
