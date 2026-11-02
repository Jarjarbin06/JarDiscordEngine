from collections.abc import Sequence

from jardiscordengine.entities.guilds import JDEEntityGuild
from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldID,
    JDEInternFieldUsername,
)
from jardiscordengine.interns.low_classes import JDEInternEntity

class JDEEntityUser(
    JDEInternEntity,
    JDEInternFieldID,
    JDEInternFieldUsername,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):
    """User entity."""

    def __init__(
        self,
        id: int,
        username: str
    ) -> None:
        """
        Initialize a new user.

        Args:
            id (int): Discord ID.
            username (str): Username.
        """

class JDEEntityClientUser(
    JDEEntityUser,
    JDEInternBaseClass[
        JDEInternInstancePolicy.SINGLETON,
        1,
        False,
    ]
):
    """Client user entity."""

class JDEEntityMember(
    JDEEntityUser,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):

    guild: JDEEntityGuild

    def __init__(
        self,
        user: JDEEntityUser,
        guild: JDEEntityGuild
    ) -> None:
        """
        Initialize a member.

        Args:
            user (JDEEntityUser): User.
            guild (JDEEntityGuild): Guild.
        """

class JDEEntityUserProfile(
    JDEInternEntity,
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        False,
    ]
):

    user: JDEEntityUser

    def __init__(
        self,
        user: JDEEntityUser
    ) -> None:
        """
        Initialize a user profile.

        Args:
            user (JDEEntityUser): User.
        """

__all__: Sequence[str] = [
    "JDEEntityClientUser",
    "JDEEntityMember",
    "JDEEntityUser",
    "JDEEntityUserProfile",
]
