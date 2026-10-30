from typing import Literal

from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.decorators import documented
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)
from jardiscordengine.interns.low_classes import (
    JDEInternField,
)

@documented
class JDEInternFieldID(
    JDEInternField,
    JDEInternBaseClass
):
    """
    ID field.

    Attributes:
        id (int): ID.
    """

    id: int

    def __init__(
        self,
        id: int
    ) -> None:
        """
        Add a ID field to the class.

        Args:
            id (int): ID.
        """

@documented
class JDEInternFieldUsername(
    JDEInternField,
    JDEInternBaseClass
):
    """
    Username field.

    Attributes:
        username (int): Username.
    """

    username: str

    def __init__(
        self,
        username: str
    ) -> None:
        """
        Add a username field to the class.

        Args:
            username (str): Username.
        """

@documented
class JDEInternFieldName(
    JDEInternField,
    JDEInternBaseClass
):
    """
    Name field.

    Attributes:
        name (str): name.
    """

    name: str

    def __init__(
        self,
        name: str
    ) -> None:
        """
        Add a name field to the class.

        Args:
            name (str): Name.
        """

@documented
class JDEInternFieldURL(
    JDEInternField,
    JDEInternBaseClass
):
    """
    URL field.

    Attributes:
        url (str): URL.
    """

    url: str

    def __init__(
        self,
        url: str
    ) -> None:
        """
        Add a URL field to the class.

        Args:
            url (str): URL.
        """

@documented
class JDEInternFieldDiscord[DiscordT](
    JDEInternField,
    JDEInternBaseClass
):
    """
    Discord field.

    Attributes:
        discord (DiscordT): Discord.
    """

    discord: DiscordT

    def __init__(
        self,
        discord: DiscordT
    ) -> None:
        """
        Add a discord field to the class.

        Args:
            discord (DiscordT): Discord object.
        """
