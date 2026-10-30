from collections.abc import Sequence
from typing import Literal, final

from discord import Bot

from jardiscordengine.bots.guild_manager import (
    JDEGuildManager,
)
from jardiscordengine.commands.command_manager import (
    JDECommandManager,
)
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
from jardiscordengine.interns.decorators import (
    documented,
    logged,
    register_entity,
    requires_init,
)
from jardiscordengine.interns.enums import JDEInternInstancePolicy
from jardiscordengine.interns.high_classes import JDEInternFieldDiscord
from jardiscordengine.systems.bool import JDEBool
from jardiscordengine.systems.version import JDEVersion

@final
@logged
@documented
@register_entity(name="JDEBot", category="Bot")
class JDEBot(
    JDEInternFieldDiscord[Bot],
    JDEInternBaseClass[
        Literal[JDEInternInstancePolicy.UNIQUE],
        Literal[0],
        Literal[True],
    ]
):
    """
    Configuration.

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
    client: JDEEntityClientUser
    intents: JDEEntityIntents
    activity: JDEEntityActivity | JDEEntityActivityGame | JDEEntityActivityStreaming | None = None
    status: JDEStatus

    @requires_init
    def __init__(
        self,
        *,
        bot_index: int = 1,
        intents: JDEEntityIntents | None = None,
        activity: JDEEntityActivity | JDEEntityActivityGame | JDEEntityActivityStreaming | None = None,
        status: JDEStatus = JDEStatus.ONLINE
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

__all__: Sequence[str] = [
    "JDEBot",
]
