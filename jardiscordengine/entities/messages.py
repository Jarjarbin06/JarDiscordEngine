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

from discord import Message as _Message

from jardiscordengine.entities.channels import JDEEntityChannel as _JDEEntityChannel
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import field as _field
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.high_classes import (
    JDEInternFieldDiscord as _JDEInternFieldDiscord,
)
from jardiscordengine.interns.high_classes import JDEInternFieldID as _JDEInternFieldID
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity


@_documented
class JDEEntityMessage(_JDEInternEntity, _JDEInternFieldID, _JDEInternFieldDiscord):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    channel = _field(_JDEEntityChannel, required=False, read_only=True, doc="Channel")

    def __new__(cls, message, channel = None, _jde_key = None, _jde_warn = None):
        message_id = message.id if isinstance(message, _Message) else message

        channel_id = (
            channel.id
            if channel is not None
            else getattr(getattr(message, "channel", None), "id", None)
        )

        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else (
                (channel_id, message_id)
                if channel_id is not None
                else message_id
            ),
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, message, channel = None):

        _assert_is_instance(message, _Message, "MESSAGE must be discord.Message",)

        message_id = message.id
        discord_message = message

        if channel is None:
            channel = message.channel

        if channel is not None:
            _assert_is_instance(channel, _JDEEntityChannel, "CHANNEL must be JDEEntityChannel")

        _JDEInternEntity.__init__(self)
        _JDEInternFieldID.__init__(self, message_id)
        _JDEInternFieldDiscord.__init__(self, discord_message)

        self.channel = channel
