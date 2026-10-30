from collections.abc import Sequence
from typing import Literal, final

from discord import Guild

from jardiscordengine.bots.bot import JDEBot
from jardiscordengine.constants import JDEFalse
from jardiscordengine.entities.categories import (
    JDEEntityGuildCategory,
)
from jardiscordengine.entities.channels import (
    JDEEntityForumChannel,
    JDEEntityStageChannel,
    JDEEntityTextChannel,
    JDEEntityVoiceChannel,
)
from jardiscordengine.entities.guilds import JDEEntityGuild
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import (
    documented,
    logged,
    register_entity,
    requires_init,
)
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)
from jardiscordengine.interns.high_classes import JDEInternFieldDiscord
from jardiscordengine.systems.bool import JDEBool

@final
@logged
@documented
@register_entity(name="JDEGuildManager", category="Manager")
class JDEGuildManager(
    JDEInternFieldDiscord[Guild],
    JDEInternBaseClass[
        Literal[JDEInternInstancePolicy.UNIQUE],
        Literal[0],
        Literal[True],
    ]
):
    """Guild manager."""

    @requires_init
    def __init__(
        self,
        bot: JDEBot,
        guild: JDEEntityGuild
    ) -> None:
        """
        Initialize a new guild manager.

        Args:
            bot (JDEBot): Bot that will handle the guild.
            guild (JDEEntityGuild): Guild.
        """

    @property
    def guild(
        self
    ) -> JDEEntityGuild:
        """
        Get managed guild.

        Returns:
            JDEEntityGuild: Guild.
        """

    async def create_category(
        self,
        name: str,
        *,
        position: int | None = None,
        reason: str | None = None
    ) -> JDEEntityGuildCategory:
        """
        Create a category.

        Args:
            name (str): Category name.
            position (int | None): Category position.
            reason (str | None): Creation reason.

        Returns:
            JDEEntityGuildCategory: Created category.
        """

    async def edit_category(
        self,
        category: int | JDEEntityGuildCategory,
        *,
        name: str | None = None,
        position: int | None = None,
        reason: str | None = None
    ) -> JDEEntityGuildCategory:
        """
        Edit a category.

        Args:
            category (int | JDEEntityGuildCategory): Category or category ID.
            name (str | None): New category name.
            position (int | None): New category position.
            reason (str | None): Edition reason.

        Returns:
            JDEEntityGuildCategory: Edited category.
        """

    async def delete_category(
        self,
        category: int | JDEEntityGuildCategory,
        *,
        reason: str | None = None
    ) -> None:
        """
        Delete a category.

        Args:
            category (int | JDEEntityGuildCategory): Category or category ID.
            reason (str | None): Deletion reason.
        """

    async def create_text_channel(
        self,
        name: str,
        *,
        category: int | JDEEntityGuildCategory | None = None,
        position: int | None = None,
        topic: str | None = None,
        slowmode_delay: int | None = None,
        nsfw: JDEBool = JDEFalse,
        reason: str | None = None
    ) -> JDEEntityTextChannel:
        """
        Create a text channel.

        Args:
            name (str): Channel name.
            category (int | JDEEntityGuildCategory | None): Channel category.
            position (int | None): Channel position.
            topic (str | None): Channel topic.
            slowmode_delay (int | None): Channel slowmode delay in seconds.
            nsfw (JDEBool): Channel NSFW status.
            reason (str | None): Creation reason.

        Returns:
            JDEEntityTextChannel: Created text channel.
        """

    async def create_voice_channel(
        self,
        name: str,
        *,
        category: int | JDEEntityGuildCategory | None = None,
        position: int | None = None,
        bitrate: int | None = None,
        user_limit: int | None = None,
        reason: str | None = None
    ) -> JDEEntityVoiceChannel:
        """
        Create a voice channel.

        Args:
            name (str): Channel name.
            category (int | JDEEntityGuildCategory | None): Channel category.
            position (int | None): Channel position.
            bitrate (int | None): Channel bit rate.
            user_limit (int | None): Channel user limit.
            reason (str | None): Creation reason.

        Returns:
            JDEEntityVoiceChannel: Created voice channel.
        """

    async def create_stage_channel(self,
        name: str,
        *,
        topic: str | None,
        category: int | JDEEntityGuildCategory | None = None,
        position: int | None = None,
        bitrate: int | None = None,
        user_limit: int | None = None,
        reason: str | None = None
    ) -> JDEEntityStageChannel:
        """
        Create a stage channel.

        Args:
            name (str): Channel name.
            topic (str | None): Channel topic.
            category (int | JDEEntityGuildCategory | None): Channel category.
            position (int | None): Channel position.
            bitrate (int | None): Channel bit rate.
            user_limit (int | None): Channel user limit.
            reason (str | None): Creation reason.

        Returns:
            JDEEntityStageChannel: Created stage channel.
        """

    async def create_forum_channel(
        self,
        name: str,
        *,
        category: int | JDEEntityGuildCategory | None = None,
        position: int | None = None,
        topic: str | None = None,
        slowmode_delay: int | None = None,
        nsfw: JDEBool = JDEFalse,
        reason: str | None = None
    ) -> JDEEntityForumChannel:
        """
        Create a forum channel.

        Args:
            name (str): Channel name.
            category (int | JDEEntityGuildCategory | None): Channel category.
            position (int | None): Channel position.
            topic (str | None): Channel topic.
            slowmode_delay (int | None): Channel slowmode delay in seconds.
            nsfw (JDEBool): Channel NSFW status.
            reason (str | None): Creation reason.

        Returns:
            JDEEntityForumChannel: Created forum channel.
        """

    async def edit_channel(
        self,
        channel: int | JDEEntityTextChannel | JDEEntityVoiceChannel | JDEEntityStageChannel | JDEEntityForumChannel,
        *,
        name: str | None = None,
        category: JDEEntityGuildCategory | None = None,
        position: int | None = None,
        topic: str | None = None,
        slowmode_delay: int | None = None,
        nsfw: JDEBool = JDEFalse,
        bitrate: int | None = None,
        user_limit: int | None = None,
        reason: str | None = None
    ) -> JDEEntityTextChannel | JDEEntityVoiceChannel | JDEEntityStageChannel | JDEEntityForumChannel:
        """
        Edit a text, voice, stage or forum channel.

        Args:
            channel (int | JDEEntityTextChannel | JDEEntityVoiceChannel | JDEEntityStageChannel | JDEEntityForumChannel): Channel or channel ID.
            name (str | None): New name.
            category (int | JDEEntityGuildCategory | None): New category.
            position (int | None): New position.
            topic (str | None): New topic.
            slowmode_delay (int | None): New slowmode delay.
            nsfw (JDEBool): New NSFW status.
            bitrate (int | None): New bit rate.
            user_limit (int | None): New user limit.
            reason (str | None): Edition reason.

        Returns:
            JDEEntityTextChannel | JDEEntityVoiceChannel | JDEEntityStageChannel | JDEEntityForumChannel: Edited channel.
        """

    async def delete_channel(
        self,
        channel: int | JDEEntityTextChannel | JDEEntityVoiceChannel | JDEEntityStageChannel | JDEEntityForumChannel,
        *,
        reason: str | None = None
    ) -> None:
        """
        Delete a text, voice, stage or forum channel.

        Args:
            channel (int | JDEEntityTextChannel | JDEEntityVoiceChannel | JDEEntityStageChannel | JDEEntityForumChannel): Channel or channel ID.
            reason (str | None): Deletion reason.
        """

__all__: Sequence[str] = [
    "JDEGuildManager",
]
