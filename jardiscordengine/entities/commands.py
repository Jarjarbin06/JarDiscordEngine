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

from discord import ApplicationContext as _ApplicationContext

from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import flag as _flag
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.high_classes import (
    JDEInternFieldDiscord as _JDEInternFieldDiscord,
)
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity


@_documented
class JDEEntityApplicationContext(_JDEInternEntity, _JDEInternFieldDiscord):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, context, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, context):
        if not isinstance(context, _ApplicationContext):
            raise TypeError(
                "CONTEXT must be a discord.ApplicationContext"
            )

        _JDEInternEntity.__init__(self)
        _JDEInternFieldDiscord.__init__(self, context)

    # Core context #

    @_flag("discord")
    def bot(self):
        return "bot"

    @_flag("discord")
    def interaction(self):
        return "interaction"

    @_flag("discord")
    def command(self):
        return "command"

    @_flag("discord")
    def cog(self):
        return "cog"

    # User and location #

    @_flag("discord")
    def user(self):
        return "user"

    @_flag("discord")
    def author(self):
        return "author"

    @_flag("discord")
    def guild(self):
        return "guild"

    @_flag("discord")
    def guild_id(self):
        return "guild_id"

    @_flag("discord")
    def channel(self):
        return "channel"

    @_flag("discord")
    def channel_id(self):
        return "channel_id"

    @_flag("discord")
    def me(self):
        return "me"

    @_flag("discord")
    def message(self):
        return "message"

    @_flag("discord")
    def voice_client(self):
        return "voice_client"

    # Localization and command options #

    @_flag("discord")
    def locale(self):
        return "locale"

    @_flag("discord")
    def guild_locale(self):
        return "guild_locale"

    @_flag("discord")
    def selected_options(self):
        return "selected_options"

    @_flag("discord")
    def unselected_options(self):
        return "unselected_options"

    @_flag("discord")
    def attachment_size_limit(self):
        return "attachment_size_limit"

    # Interaction response objects #

    @_flag("discord")
    def response(self):
        return "response"

    @_flag("discord")
    def followup(self):
        return "followup"

    # Interaction response methods #

    @_flag("discord")
    def respond(self):
        return "respond"

    @_flag("discord")
    def send_response(self):
        return "send_response"

    @_flag("discord")
    def send_followup(self):
        return "send_followup"

    @_flag("discord")
    def send_modal(self):
        return "send_modal"

    @_flag("discord")
    def defer(self):
        return "defer"

    @_flag("discord")
    def edit(self):
        return "edit"

    @_flag("discord")
    def delete(self):
        return "delete"

    # Command invocation #

    @_flag("discord")
    def invoke(self):
        return "invoke"

    # Installation authorization #

    @_flag("discord")
    def is_guild_authorised(self):
        return "is_guild_authorised"

    @_flag("discord")
    def is_guild_authorized(self):
        return "is_guild_authorized"

    @_flag("discord")
    def is_user_authorised(self):
        return "is_user_authorised"

    @_flag("discord")
    def is_user_authorized(self):
        return "is_user_authorized"

    # Inherited Messageable interface #

    @_flag("discord")
    def send(self):
        return "send"

    @_flag("discord")
    def fetch_message(self):
        return "fetch_message"

    @_flag("discord")
    def history(self):
        return "history"

    @_flag("discord")
    def pins(self):
        return "pins"

    @_flag("discord")
    def typing(self):
        return "typing"

    @_flag("discord")
    def trigger_typing(self):
        return "trigger_typing"
