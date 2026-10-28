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

from discord import Activity as _Activity
from discord import Game as _Game
from discord import Intents as _Intents
from discord import PartialEmoji as _PartialEmoji
from discord import Streaming as _Streaming

from jardiscordengine.entities.enums import JDEActivityType
from jardiscordengine.interns import JTKExternTime as _JTKExternTime
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import flag as _flag
from jardiscordengine.interns.decorators import handle_errors as _handle_errors
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldDiscord as _JDEInternFieldDiscord,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldName as _JDEInternFieldName,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldURL as _JDEInternFieldURL,
)
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity
from jardiscordengine.systems.bool import JDEBool as _JDEBool


@_documented
class JDEEntityIntents(_JDEInternEntity, _JDEInternFieldDiscord):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, _jde_key = None, _jde_warn = None, **kwargs):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, **kwargs):
        _JDEInternEntity.__init__(self)
        _JDEInternFieldDiscord.__init__(self, _Intents(**kwargs))


    @classmethod
    def default(cls):
        return cls._from_discord_intents(_Intents.default())

    @classmethod
    def all(cls):
        return cls._from_discord_intents(_Intents.all())

    @classmethod
    def none(cls):
        return cls._from_discord_intents(_Intents.none())

    @classmethod
    @_handle_errors
    def _from_discord_intents(cls, discord_intents):
        instance = cls.__new__(cls)
        _JDEInternEntity.__init__(instance)
        _JDEInternFieldDiscord.__init__(instance, discord_intents)
        return instance

    # Guild, membership, and moderation #

    @_flag("discord", cast=_JDEBool)
    def guilds(self):
        return "guilds"

    @_flag("discord", cast=_JDEBool)
    def members(self):
        return "members"

    @_flag("discord", cast=_JDEBool)
    def moderation(self):
        return "moderation"

    @_flag("discord", cast=_JDEBool)
    def emojis_and_stickers(self):
        return "emojis_and_stickers"

    @_flag("discord", cast=_JDEBool)
    def integrations(self):
        return "integrations"

    @_flag("discord", cast=_JDEBool)
    def webhooks(self):
        return "webhooks"

    @_flag("discord", cast=_JDEBool)
    def invites(self):
        return "invites"

    @_flag("discord", cast=_JDEBool)
    def scheduled_events(self):
        return "scheduled_events"

    @_flag("discord", cast=_JDEBool)
    def auto_moderation_configuration(self):
        return "auto_moderation_configuration"

    @_flag("discord", cast=_JDEBool)
    def auto_moderation_execution(self):
        return "auto_moderation_execution"

    # Messages, reactions, and typing #

    @_flag("discord", cast=_JDEBool)
    def messages(self):
        return "messages"

    @_flag("discord", cast=_JDEBool)
    def guild_messages(self):
        return "guild_messages"

    @_flag("discord", cast=_JDEBool)
    def dm_messages(self):
        return "dm_messages"

    @_flag("discord", cast=_JDEBool)
    def guild_reactions(self):
        return "guild_reactions"

    @_flag("discord", cast=_JDEBool)
    def dm_reactions(self):
        return "dm_reactions"

    @_flag("discord", cast=_JDEBool)
    def guild_typing(self):
        return "guild_typing"

    @_flag("discord", cast=_JDEBool)
    def dm_typing(self):
        return "dm_typing"

    @_flag("discord", cast=_JDEBool)
    def message_content(self):
        return "message_content"

    @_flag("discord", cast=_JDEBool)
    def guild_polls(self):
        return "guild_polls"

    @_flag("discord", cast=_JDEBool)
    def dm_polls(self):
        return "dm_polls"

    # Voice and presence #

    @_flag("discord", cast=_JDEBool)
    def voice_states(self):
        return "voice_states"

    @_flag("discord", cast=_JDEBool)
    def presences(self):
        return "presences"

@_documented
class JDEEntityActivity(_JDEInternEntity, _JDEInternFieldName, _JDEInternFieldDiscord):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, _jde_key = None, _jde_warn = None, **kwargs):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, **kwargs):
        _JDEInternEntity.__init__(self)

        """
        :TODO:
            REMAINING FROM DISCORD:

                self.assets: ActivityAssets = kwargs.pop("assets", {})
                self.party: ActivityParty = kwargs.pop("party", {})
                self.application_id: int | None = _get_as_snowflake(kwargs, "application_id")
                self.url: str | None = kwargs.pop("url", None)
                self.flags: int = kwargs.pop("flags", 0)
                self.sync_id: str | None = kwargs.pop("sync_id", None)
                self.session_id: str | None = kwargs.pop("session_id", None)
                self.buttons: list[str] = kwargs.pop("buttons", [])
        """

        created_at = int(_JTKExternTime.Time().timestamp() * 1000)
        state = kwargs.pop("state", None)
        details = kwargs.pop("details", None)
        timestamps = {
            "start": int(kwargs.pop("start", _JTKExternTime.Time().timestamp()) * 1000),
            "end": int(kwargs.pop("end", _JTKExternTime.Time().timestamp()) * 1000),
        }

        type = kwargs.pop("type", -1)
        name = kwargs.pop("name", "JDECustomStatus" if type == JDEActivityType.CUSTOM else None)
        _emoji = kwargs.pop("emoji", None)
        emoji = _PartialEmoji.from_str(_emoji.emoji) if _emoji is not None else None

        _JDEInternFieldName.__init__(self, name or "Activity")
        _JDEInternFieldDiscord.__init__(self, _Activity(
            created_at=created_at,
            state=state,
            details=details,
            timestamps=timestamps,

            type=type,
            name=name,
            emoji=emoji,
        ))

    @property
    @_handle_errors
    def start(self):
        return _JTKExternTime.Time(timestamp=self.discord.start.timestamp())  # pyright: ignore[reportAttributeAccessIssue]

    @property
    @_handle_errors
    def end(self):
        return _JTKExternTime.Time(timestamp=self.discord.end.timestamp())  # pyright: ignore[reportAttributeAccessIssue]

@_documented
class JDEEntityActivityGame(_JDEInternEntity, _JDEInternFieldName, _JDEInternFieldDiscord):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, name, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, name):
        _JDEInternEntity.__init__(self)
        _JDEInternFieldName.__init__(self, name)
        _JDEInternFieldDiscord.__init__(self, _Game(name))

@_documented
class JDEEntityActivityStreaming(_JDEInternEntity, _JDEInternFieldName, _JDEInternFieldDiscord, _JDEInternFieldURL):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, name, url, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, name, url):
        _JDEInternEntity.__init__(self)
        _JDEInternFieldURL.__init__(self, url)
        _JDEInternFieldName.__init__(self, name)
        _JDEInternFieldDiscord.__init__(self, _Streaming(name=name, url=url))
