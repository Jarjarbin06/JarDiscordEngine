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

import asyncio as _asyncio
import os as _os
from typing import final as _final

import discord as _discord
from discord import Bot as _Bot

from jardiscordengine.bots.guild_manager import (
    JDEGuildManager as _JDEGuildManager,
)
from jardiscordengine.entities.bots import JDEEntityActivity as _JDEEntityActivity
from jardiscordengine.entities.bots import (
    JDEEntityActivityGame as _JDEEntityActivityGame,
)
from jardiscordengine.entities.bots import (
    JDEEntityActivityStreaming as _JDEEntityActivityStreaming,
)
from jardiscordengine.entities.bots import JDEEntityIntents as _JDEEntityIntents
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
from jardiscordengine.entities.enums import JDEStatus as _JDEStatus
from jardiscordengine.entities.guilds import JDEEntityGuild as _JDEEntityGuild
from jardiscordengine.entities.messages import JDEEntityMessage as _JDEEntityMessage
from jardiscordengine.entities.roles import JDEEntityRole as _JDEEntityRole
from jardiscordengine.entities.users import JDEEntityClientUser as _JDEEntityClientUser
from jardiscordengine.entities.users import JDEEntityUser as _JDEEntityUser
from jardiscordengine.interns.config import CONFIGS as _CONFIGS
from jardiscordengine.interns.config import get as _get
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import field as _field
from jardiscordengine.interns.decorators import flag as _flag
from jardiscordengine.interns.decorators import logged as _logged
from jardiscordengine.interns.decorators import register_entity as _register_entity
from jardiscordengine.interns.decorators import requires_init as _requires_init
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldDiscord as _JDEInternFieldDiscord,
)


@_final
@_logged
@_documented
@_register_entity(name="JDEBot", category="Bot")
class JDEBot(_JDEInternFieldDiscord):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    name = _field(str, required=True, read_only=True, doc="Name")
    description = _field(str, required=True, read_only=True, doc="Description")
    application_id = _field(int | None, read_only=True, doc="Application ID")
    owners = _field(tuple | None, read_only=True, doc="Owners")
    debug_guilds = _field(tuple | None, read_only=True, doc="Debug guilds")
    client = _field(_JDEEntityClientUser, required=True, read_only=True, doc="Client")
    intents = _field(_JDEEntityIntents, required=True, read_only=True, doc="Intents")
    activity = _field(_JDEEntityActivity | _JDEEntityActivityGame | _JDEEntityActivityStreaming | None, read_only=True, doc="Activity")
    status = _field(_JDEStatus, read_only=True, doc="Status")

    @_requires_init
    def __new__(cls, bot_index = 1, _jde_key = None, _jde_warn = None, **kwargs):
        return _JDEInternFieldDiscord.__new__(
            cls,
            _jde_key=bot_index,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    @_requires_init
    def __init__(self, *, bot_index = 1, intents = None, activity = None, status = _JDEStatus.ONLINE):
        if hasattr(self, "_initialized"):
            return

        def init_from_env():
            if "JDE_TOKEN" not in _os.environ:
                raise RuntimeError("JDE_TOKEN not found in environment")

            self._token = _os.environ.get("JDE_TOKEN")  # pyright: ignore[reportAttributeAccessIssue]

        def init_from_config():
            if not _CONFIGS["bots"].section_exists(str(bot_index)):
                raise RuntimeError(f"Bot {bot_index} doesn't exist in the bot config")

            self.name = _get("bots", str(bot_index), "name", str, "JDEBot")
            self.description = _get("bots", str(bot_index), "description", str, "")
            self.application_id = _get("bots", str(bot_index), "application_id", int, 0) or None

            owners = _get("bots", str(bot_index), "owners_id", str, "").split(",")
            if owners and owners[0] != "":
                self.owners = tuple(_JDEEntityUser(int(id), f"Owner({id})") for id in owners)
            else:
                self.owners = None

            debug_guilds = _get("bots", str(bot_index), "debug_guild_id", str, "").split(",")
            if debug_guilds and debug_guilds[0] != "":
                self.debug_guilds = tuple(_JDEEntityGuild(int(id), f"DebugGuild({id})", _jde_warn=False) for id in debug_guilds)  # pyright: ignore[reportCallIssue]
            else:
                self.debug_guilds = None

            self.client = _JDEEntityClientUser(_get("bots", str(bot_index), "client_id", int, 0), self.name)

        def init_bot():
            kwargs = {}

            if self.application_id is not None:
                kwargs["application_id"] = self.application_id

            if self.owners is not None:
                owners_count = len(self.owners)  # pyright: ignore[reportArgumentType]
                if owners_count == 1:
                    kwargs["owner_id"] = self.owners[0].id  # pyright: ignore[reportIndexIssue]
                elif owners_count > 1:
                    kwargs["owner_ids"] = [owner.id for owner in self.owners]  # pyright: ignore[reportGeneralTypeIssues]

            if self.debug_guilds:
                kwargs["debug_guilds"] = [guild.id for guild in self.debug_guilds]  # pyright: ignore[reportIndexIssue, reportGeneralTypeIssues]

            kwargs["intents"] = self.intents.discord  # pyright: ignore[reportAttributeAccessIssue]
            kwargs["status"] = self.status
            kwargs["activity"] = self.activity.discord if self.activity is not None else None  # pyright: ignore[reportAttributeAccessIssue]

            bot = _Bot(self.description, **kwargs)

            _JDEInternFieldDiscord.__init__(self, bot)

            self.discord.add_listener(  # pyright: ignore[reportAttributeAccessIssue]
                self._synchronize_entities,  # pyright: ignore[reportAttributeAccessIssue]
                "on_ready",
            )

        self._synchronized = False
        self._synchronization_event = _asyncio.Event()
        self._synchronization_error = None

        self._guilds = {}
        self._channels = {}
        self._roles = {}
        self._messages = {}

        self.intents = intents or _JDEEntityIntents.default()
        self.activity = activity
        self.status = status

        init_from_env()
        init_from_config()
        init_bot()

        self._initialized = True

    async def _synchronize_entities(self):
        if self.synchronized:
            return

        try:
            for discord_guild in self.discord.guilds:  # pyright: ignore[reportAttributeAccessIssue]
                guild = _JDEEntityGuild(
                    discord_guild.id,
                    discord_guild.name,
                    _jde_warn=False  # pyright: ignore[reportCallIssue]
                )

                self._guilds[discord_guild.id] = guild

                for discord_role in discord_guild.roles:
                    role = _JDEEntityRole(
                        discord_role.id,
                        discord_role.name,
                    )

                    self._roles[discord_role.id] = role

                for discord_channel in discord_guild.channels:
                    if isinstance(discord_channel, _discord.CategoryChannel):
                        channel = _JDEEntityGuildCategory(
                            discord_channel,
                            guild,
                            _jde_warn=False,  # pyright: ignore[reportCallIssue]
                        )

                    elif isinstance(discord_channel, _discord.TextChannel):
                        channel = _JDEEntityTextChannel(
                            discord_channel,
                            guild,
                            _jde_warn=False,  # pyright: ignore[reportCallIssue]
                        )

                    elif isinstance(discord_channel, _discord.VoiceChannel):
                        channel = _JDEEntityVoiceChannel(
                            discord_channel,
                            guild,
                            _jde_warn=False,  # pyright: ignore[reportCallIssue]
                        )

                    elif isinstance(discord_channel, _discord.StageChannel):
                        channel = _JDEEntityStageChannel(
                            discord_channel,
                            guild,
                            _jde_warn=False,  # pyright: ignore[reportCallIssue]
                        )

                    elif isinstance(discord_channel, _discord.ForumChannel):
                        channel = _JDEEntityForumChannel(
                            discord_channel,
                            guild,
                            _jde_warn=False,  # pyright: ignore[reportCallIssue]
                        )

                    else:
                        channel = _JDEEntityGuildChannel(
                            discord_channel,
                            guild,
                            _jde_warn=False,  # pyright: ignore[reportCallIssue]
                        )

                    self._channels[discord_channel.id] = channel

                    if not isinstance(discord_channel, _discord.TextChannel):
                        continue

                    async for discord_message in discord_channel.history(
                        limit=None,
                        oldest_first=True,
                    ):
                        message = _JDEEntityMessage(
                            discord_message,
                            channel=channel,
                        )

                        self._messages[discord_message.id] = message

            self._synchronized = True

        except Exception as error:
            self._synchronization_error = error
            raise

        finally:
            self._synchronization_event.set()

    async def wait_until_synchronized(self):
        await self._synchronization_event.wait()

        if self._synchronization_error is not None:
            raise RuntimeError(
                "Discord entity synchronization failed."
            ) from self._synchronization_error

        if not self.synchronized:
            raise RuntimeError(
                "Discord entity synchronization did not complete."
            )

    @_flag(doc="Guild list")
    def guilds(self):
        return "_guilds"

    @_flag(doc="Role list")
    def roles(self):
        return "_roles"

    @_flag(doc="Channel list")
    def channels(self):
        return "_channels"

    @_flag(doc="Message history")
    def messages(self):
        return "_messages"

    def guild(self, guild):
        if not self.synchronized:
            raise RuntimeError(
                "Cannot manage guilds before entity synchronization completes."
            )

        guild = self._guilds.get(guild.id)

        if guild is None:
            raise LookupError(
                f"Guild {guild.id} is not registered with this bot."  # pyright: ignore[reportAttributeAccessIssue]
            )

        return _JDEGuildManager(self, guild)

    async def change_presence(self, *, status = None, activity = None):
        self._jde_initializing = True
        try:
            self.activity = activity or self.activity
            self.status = status or self.status
        finally:
            self._jde_initializing = False

        await self.discord.change_presence(status=status, activity=activity)  # pyright: ignore[reportAttributeAccessIssue]

    async def start(self):
        await self.discord.start(self._token)  # pyright: ignore[reportAttributeAccessIssue]

    async def close(self):
        await self.discord.close()  # pyright: ignore[reportAttributeAccessIssue]

    @_flag(cast=bool)
    def synchronized(self):
        return "_synchronized"
