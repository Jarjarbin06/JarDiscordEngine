from collections.abc import Sequence
from typing import Any, Literal, final

from discord import Bot

from jardiscordengine.entities.bots import (
    JDEEntityActivity,
    JDEEntityActivityGame,
    JDEEntityActivityStreaming,
    JDEEntityIntents,
)
from jardiscordengine.entities.categories import (
    JDEEntityGuildCategory,
)
from jardiscordengine.entities.channels import (
    JDEEntityGuildChannel,
)
from jardiscordengine.entities.enums import JDEStatus
from jardiscordengine.entities.guilds import JDEEntityGuild
from jardiscordengine.entities.messages import JDEEntityMessage
from jardiscordengine.entities.roles import JDEEntityRole
from jardiscordengine.entities.users import JDEEntityClientUser, JDEEntityUser
from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.enums import JDEInternInstancePolicy
from jardiscordengine.interns.high_classes import JDEInternFieldDiscord
from jardiscordengine.managers.command_manager import (
    JDECommandManager,
)
from jardiscordengine.managers.guild_manager import (
    JDEGuildManager,
)
from jardiscordengine.systems.bool import JDEBool
from jardiscordengine.systems.version import JDEVersion

@final
class JDEBot(
    JDEInternFieldDiscord[Bot],
    JDEInternBaseClass[
        JDEInternInstancePolicy.UNIQUE,
        0,
        True,
    ]
):
    """
    Bot.

    Attributes:
        name (str): Bot name.
        version (JDEVersion): Bot version.
        description (str): Bot description.
        application_id (int | None): Bot application id (same as client ID).
        owners (tuple[JDEEntityUser] | None): Bot owners (who have all permissions on the bot).
        debug_guilds (tuple[JDEEntityGuild] | None): Bot debug guilds (used for tests).
        client (JDEEntityClientUser): User entity of the bot.
        intents (JDEEntityIntents): Intents of the bot.
        activity (JDEEntityActivity | JDEEntityActivityGame | JDEEntityActivityStreaming | None): Current activity of the bot.
        status (JDEStatus): Status of the bot.
    """

    name: str
    version: JDEVersion
    description: str
    application_id: int | None = None
    owners: tuple[JDEEntityUser] | None = None
    debug_guilds: tuple[JDEEntityGuild] | None = None
    bot_guilds: tuple[JDEEntityGuild] | None = None
    client: JDEEntityClientUser
    intents: JDEEntityIntents
    activity: JDEEntityActivity | JDEEntityActivityGame | JDEEntityActivityStreaming | None = None
    status: JDEStatus

    def __init__(
        self,
        *,
        bot_index: int = 1,
        intents: JDEEntityIntents | None = None,
        activity: JDEEntityActivity | JDEEntityActivityGame | JDEEntityActivityStreaming | None = None,
        status: JDEStatus = JDEStatus.ONLINE,
        no_sync: tuple[Literal["MESSAGES"], ...] = ()
    ) -> None:
        """
        Initialize a new bot.

        Args:
            bot_index (int): Bot config index to load.
            intents (JDEEntityIntents | None): Description, optional (default: None).
            activity (JDEEntityActivity | JDEEntityActivityGame | JDEEntityActivityStreaming | None): Description, optional (default: None).
            status (JDEStatus): Description, optional (default: JDEStatus.ONLINE).
        """

    @property
    def command_manager(
        self
    ) -> JDECommandManager:
        """
        Get the command manager.

        Returns:
            JDECommandManager: Command manager.
        """

    async def wait_until_synchronized(
        self
    ) -> None:
        """Wait for bot to fully startup."""

    @property
    def guilds(
        self
    ) -> dict[int, JDEEntityGuild]:
        """
        Get the synchronized guild list.

        Returns:
            list[JDEEntityGuild]: Guild list.
        """

    @property
    def categories(
        self
    ) -> dict[int, JDEEntityGuildCategory]:
        """
        Get the synchronized category dictionary.

        Returns:
            dict[int, JDEEntityGuildCategory]: Category dictionary.
        """

    @property
    def channels(
        self
    ) -> dict[int, JDEEntityGuildChannel]:
        """
        Get the synchronized channel list.

        Returns:
            dict[int, JDEEntityGuildChannel]: Channel dictionary.
        """

    @property
    def messages(
        self
    ) -> dict[int, JDEEntityMessage]:
        """
        Get the synchronized message list.

        Returns:
            dict[int, JDEEntityMessage]: Message dictionary.
        """

    @property
    def roles(
        self
    ) -> dict[int, JDEEntityRole]:
        """
        Get the synchronized role list.

        Returns:
            dict[int, JDEEntityRole]: Role dictionary.
        """

    def guild(
        self,
        guild: JDEEntityGuild
    ) -> JDEGuildManager:
        """
        Get the guild manager for a guild.

        Args:
            guild (JDEEntityGuild): Guild to manage.

        Returns:
            JDEGuildManager: Guild manager.
        """

    async def change_presence(
        self,
        *,
        status: JDEStatus | None = None,
        activity: JDEEntityActivity | JDEEntityActivityGame | JDEEntityActivityStreaming | None = None
    ) -> None:
        """
        Change bot presence.

        Args:
            status (JDEStatus | None): New status of the bot.
            activity (JDEEntityActivity): New activity of the bot.
        """

    @property
    def synchronized(
        self
    ) -> JDEBool:
        """
        Get if the bot is synchronized.

        Returns:
            JDEBool: Is synchronized.
        """

    def sync_commands(
        self
    ) -> Any:
        """Synchronize discord commands."""

__all__: Sequence[str] = [
    "JDEBot",
]
