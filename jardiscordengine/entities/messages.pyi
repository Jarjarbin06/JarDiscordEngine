from discord import Message

from jardiscordengine.entities.channels import JDEEntityChannel
from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.decorators import documented, field
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance
from jardiscordengine.interns.high_classes import (
    JDEInternFieldDiscord,
    JDEInternFieldID,
)
from jardiscordengine.interns.low_classes import JDEInternEntity

class JDEEntityMessage(
    JDEInternEntity,
    JDEInternFieldID,
    JDEInternFieldDiscord,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """
    Message entity.

    Attributes:
        channel (JDEEntityChannel | None): Channel entity
    """

    channel: JDEEntityChannel | None

    def __init__(
        self,
        message: str,
        channel: JDEEntityChannel | None = None
    ) -> None:
        """
        Initialize a message.

        Args:
            message (str): Description.
            channel (JDEEntityChannel | None): Description, optional (default: None).
        """

__all__ = [
    "JDEEntityMessage",
]
