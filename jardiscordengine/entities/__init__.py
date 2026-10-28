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

from jardiscordengine.entities.assets import (
    JDEEntityAvatar,
    JDEEntityBanner,
    JDEEntityCustomEmoji,
    JDEEntityEmoji,
    JDEEntityGuildIcon,
    JDEEntityImage,
    JDEEntitySticker,
)
from jardiscordengine.entities.bots import (
    JDEEntityActivity,
    JDEEntityActivityGame,
    JDEEntityActivityStreaming,
    JDEEntityIntents,
)
from jardiscordengine.entities.categories import (
    JDEEntityCategory,
    JDEEntityGuildCategory,
)
from jardiscordengine.entities.channels import (
    JDEEntityAnnouncementChannel,
    JDEEntityChannel,
    JDEEntityForumChannel,
    JDEEntityGuildChannel,
    JDEEntityStageChannel,
    JDEEntityTextChannel,
    JDEEntityVoiceChannel,
)
from jardiscordengine.entities.enums import (
    JDEActivityType,
    JDEStatus,
)
from jardiscordengine.entities.guilds import (
    JDEEntityGuild,
)
from jardiscordengine.entities.messages import (
    JDEEntityMessage,
)
from jardiscordengine.entities.roles import (
    JDEEntityRole,
)
from jardiscordengine.entities.users import (
    JDEEntityClientUser,
    JDEEntityMember,
    JDEEntityUser,
    JDEEntityUserProfile,
)
from jardiscordengine.entities.webhook import (
    JDEEntityWebhook,
    JDEEntityWebhookEmbed,
    JDEEntityWebhookMessage,
)

__all__ = [
    "JDEActivityType",
    "JDEEntityActivity",
    "JDEEntityActivityGame",
    "JDEEntityActivityStreaming",
    "JDEEntityAnnouncementChannel",
    "JDEEntityAvatar",
    "JDEEntityBanner",
    "JDEEntityCategory",
    "JDEEntityChannel",
    "JDEEntityClientUser",
    "JDEEntityCustomEmoji",
    "JDEEntityEmoji",
    "JDEEntityForumChannel",
    "JDEEntityGuild",
    "JDEEntityGuildCategory",
    "JDEEntityGuildChannel",
    "JDEEntityGuildIcon",
    "JDEEntityImage",
    "JDEEntityIntents",
    "JDEEntityMember",
    "JDEEntityMessage",
    "JDEEntityRole",
    "JDEEntityStageChannel",
    "JDEEntitySticker",
    "JDEEntityTextChannel",
    "JDEEntityUser",
    "JDEEntityUserProfile",
    "JDEEntityVoiceChannel",
    "JDEEntityWebhook",
    "JDEEntityWebhookEmbed",
    "JDEEntityWebhookMessage",
    "JDEStatus",
]
