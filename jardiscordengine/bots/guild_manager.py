# =============================================================================
# JarDiscordEngine - Python Discord Bot Engine (pycord-based)
# =============================================================================
#
# JarDiscordEngine is a lightweight bot framework built on top of pycord
# that simplifies Discord bot development while providing higher-level
# abstractions for command management, event handling, and extensibility.
#
# =============================================================================
# Version: jardiscordengine-v1
# Author: Jarjarbin Studio
# License: GPL v3
# =============================================================================
#
# This engine is inspired by pycord, modern bot framework design patterns,
# and modular software architecture.
#
# It is designed for educational purposes and small-to-medium Discord bot
# projects.
#
# It provides structured systems such as automatic command discovery,
# command registration, event handling, extension management, and shared
# services for logging, configuration, and permissions.
#
# =============================================================================
# WARNING:
# =============================================================================
#
# This is NOT pycord itself.
# It is a custom abstraction layer built on top of pycord.
#
# =============================================================================

from __future__ import annotations

import discord as _discord

from jardiscordengine.entities.categories import (
    JDEEntityGuildCategory as _JDEEntityGuildCategory,
)
from jardiscordengine.entities.channels import (
    JDEEntityForumChannel as _JDEEntityForumChannel,
)
from jardiscordengine.entities.channels import (
    JDEEntityGuildChannel as _JDEEntityGuildChannel,
)
from jardiscordengine.entities.channels import (
    JDEEntityStageChannel as _JDEEntityStageChannel,
)
from jardiscordengine.entities.channels import (
    JDEEntityTextChannel as _JDEEntityTextChannel,
)
from jardiscordengine.entities.channels import (
    JDEEntityVoiceChannel as _JDEEntityVoiceChannel,
)


class JDEGuildManager:

    def __init__(self, bot, guild):
        self._bot = bot
        self._guild = guild

        self._get_discord_guild()

    @property
    def guild(self):
        return self._guild

    @property
    def discord(self):
        return self._get_discord_guild()

    def _get_discord_guild(self):
        discord_guild = self._bot.discord.get_guild(self._guild.id)

        if discord_guild is None:
            raise RuntimeError(
                f"Discord guild {self._guild.id} is not available "
                "to this bot."
            )

        return discord_guild

    @staticmethod
    def _entity_type(channel):
        if isinstance(channel, _discord.TextChannel):
            return _JDEEntityTextChannel

        if isinstance(channel, _discord.VoiceChannel):
            return _JDEEntityVoiceChannel

        if isinstance(channel, _discord.StageChannel):
            return _JDEEntityStageChannel

        if isinstance(channel, _discord.ForumChannel):
            return _JDEEntityForumChannel

        return _JDEEntityGuildChannel

    def _synchronize_channel(self, discord_channel):
        channel_id = discord_channel.id
        entity_type = self._entity_type(discord_channel)
        channel = self._bot.channels.get(channel_id)

        if channel is not None and isinstance(channel, entity_type):
            channel.discord = discord_channel
            channel.name = discord_channel.name

            return channel

        channel = entity_type(
            discord_channel,
            self._guild,
            _jde_warn=False,  # pyright: ignore[reportCallIssue]
        )

        self._bot.channels[channel_id] = channel

        return channel

    def _synchronize_category(self, discord_category):
        category_id = discord_category.id
        category = self._bot.channels.get(category_id)

        if isinstance(category, _JDEEntityGuildCategory):
            category.discord = discord_category
            category.name = discord_category.name

            return category

        category = _JDEEntityGuildCategory(
            discord_category,
            self._guild,
            _jde_warn=False,  # pyright: ignore[reportCallIssue]
        )
        self._bot.channels[category_id] = category

        return category

    def _remove_channel(self, channel_id):
        self._bot.channels.pop(channel_id, None)

        message_ids = [
            message_id
            for message_id, message in self._bot.messages.items()
            if getattr(getattr(message, "channel", None), "id", None)
            == channel_id
        ]

        for message_id in message_ids:
            self._bot.messages.pop(message_id, None)

    def _resolve_category(self, category):
        if isinstance(category, _JDEEntityGuildCategory):
            if category.guild.id != self._guild.id:  # pyright: ignore[reportAttributeAccessIssue]
                raise ValueError(
                    "The specified category belongs to another guild."
                )

            category_id = category.id
        elif isinstance(category, int):
            category_id = category
        else:
            raise TypeError(
                "CATEGORY must be a category ID or JDEEntityGuildCategory."
            )

        discord_category = self._get_discord_guild().get_channel(
            category_id
        )

        if not isinstance(discord_category, _discord.CategoryChannel):
            raise TypeError(
                f"Category {category_id} was not found in guild "
                f"{self._guild.id}."
            )

        return discord_category

    def _resolve_channel(self, channel):
        channel_id = channel if isinstance(channel, int) else channel.id
        discord_channel = self._get_discord_guild().get_channel(channel_id)

        if discord_channel is None:
            raise LookupError(
                f"Channel {channel_id} was not found in guild "
                f"{self._guild.id}."
            )

        if not isinstance(discord_channel, _discord.abc.GuildChannel):
            raise TypeError(
                f"Channel {channel_id} is not a guild channel."
            )

        return discord_channel

    async def create_category(self, name, *, position = None, reason = None):
        discord_category = await self._get_discord_guild().create_category(
            name,
            position=position,
            reason=reason,
        )

        return self._synchronize_category(discord_category)

    async def edit_category(self, category, *, name = None, position = None, reason = None):
        discord_category = self._resolve_category(category)

        options = {}

        if name is not None:
            options["name"] = name

        if position is not None:
            options["position"] = position

        if reason is not None:
            options["reason"] = reason

        if options:
            discord_category = await discord_category.edit(**options)

        return self._synchronize_category(discord_category)

    async def delete_category(self, category, *, reason = None):
        discord_category = self._resolve_category(category)
        guild = self._get_discord_guild()

        child_channel_ids = [
            channel.id
            for channel in discord_category.channels
        ]
        category_id = discord_category.id

        await discord_category.delete(reason=reason)

        self._remove_channel(category_id)

        for channel_id in child_channel_ids:
            child_channel = guild.get_channel(channel_id)

            if child_channel is not None:
                self._synchronize_channel(child_channel)

    async def create_text_channel(self, name, *, category = None, position = None, topic = None, slowmode_delay = None, nsfw = None, reason = None):
        options = {}

        if category is not None:
            options["category"] = self._resolve_category(category)

        if position is not None:
            options["position"] = position

        if topic is not None:
            options["topic"] = topic

        if slowmode_delay is not None:
            options["slowmode_delay"] = slowmode_delay

        if nsfw is not None:
            options["nsfw"] = nsfw

        if reason is not None:
            options["reason"] = reason

        discord_channel = await self._get_discord_guild().create_text_channel(
            name,
            **options,
        )

        return self._synchronize_channel(discord_channel)

    async def create_voice_channel(self, name, *, category = None, position = None, bitrate = None, user_limit = None, reason = None):
        options = {}

        if category is not None:
            options["category"] = self._resolve_category(category)

        if position is not None:
            options["position"] = position

        if bitrate is not None:
            options["bitrate"] = bitrate

        if user_limit is not None:
            options["user_limit"] = user_limit

        if reason is not None:
            options["reason"] = reason

        discord_channel = await self._get_discord_guild().create_voice_channel(
            name,
            **options,
        )

        return self._synchronize_channel(discord_channel)

    async def create_stage_channel(self, name, *, topic, category = None, position = None, bitrate = None, user_limit = None, reason = None):
        options = {
            "topic": topic,
        }

        if category is not None:
            options["category"] = self._resolve_category(category)

        if position is not None:
            options["position"] = position

        if bitrate is not None:
            options["bitrate"] = bitrate

        if user_limit is not None:
            options["user_limit"] = user_limit

        if reason is not None:
            options["reason"] = reason

        discord_channel = await self._get_discord_guild().create_stage_channel(
            name,
            **options,
        )

        return self._synchronize_channel(discord_channel)

    async def create_forum_channel(self, name, *, category = None, position = None, topic = None, slowmode_delay = None, nsfw = None, reason = None):
        options = {}

        if category is not None:
            options["category"] = self._resolve_category(category)

        if position is not None:
            options["position"] = position

        if topic is not None:
            options["topic"] = topic

        if slowmode_delay is not None:
            options["slowmode_delay"] = slowmode_delay

        if nsfw is not None:
            options["nsfw"] = nsfw

        if reason is not None:
            options["reason"] = reason

        discord_channel = await self._get_discord_guild().create_forum_channel(
            name,
            **options,
        )

        return self._synchronize_channel(discord_channel)

    async def edit_channel(self, channel, *, name = None, category = None, position = None, topic = None, slowmode_delay = None, nsfw = None, bitrate = None, user_limit = None, reason = None):
        discord_channel = self._resolve_channel(channel)

        options = {}

        if name is not None:
            options["name"] = name

        if category is not None:
            options["category"] = self._resolve_category(category)

        if position is not None:
            options["position"] = position

        if topic is not None:
            options["topic"] = topic

        if slowmode_delay is not None:
            options["slowmode_delay"] = slowmode_delay

        if nsfw is not None:
            options["nsfw"] = nsfw

        if bitrate is not None:
            options["bitrate"] = bitrate

        if user_limit is not None:
            options["user_limit"] = user_limit

        if reason is not None:
            options["reason"] = reason

        if options:
            discord_channel = await discord_channel.edit(**options)  # pyright: ignore[reportAttributeAccessIssue]

        return self._synchronize_channel(discord_channel)

    async def delete_channel(self, channel, *, reason = None):
        discord_channel = self._resolve_channel(channel)
        channel_id = discord_channel.id

        await discord_channel.delete(reason=reason)

        self._remove_channel(channel_id)
