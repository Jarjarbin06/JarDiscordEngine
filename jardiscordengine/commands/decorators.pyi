from collections.abc import Awaitable, Callable, Sequence
from typing import Concatenate, Literal, TypedDict, Unpack

from jardiscordengine.bots.bot import JDEBot
from jardiscordengine.entities.commands import JDEEntityApplicationContext

type JDECommand[**P] = Callable[Concatenate[JDEBot, JDEEntityApplicationContext, P], Awaitable[None]]
type JDECommandDecorator[**P] = Callable[[JDECommand[P]], JDECommand[P]]

class JDEPermissionOptions(TypedDict, total=False):
    administrator: bool
    add_reactions: bool
    attach_files: bool
    ban_members: bool
    bypass_slowmode: bool
    change_nickname: bool
    connect: bool
    create_instant_invite: bool
    create_private_threads: bool
    create_public_threads: bool
    deafen_members: bool
    embed_links: bool
    external_emojis: bool
    external_stickers: bool
    kick_members: bool
    manage_channels: bool
    manage_emojis: bool
    manage_events: bool
    manage_guild: bool
    manage_messages: bool
    manage_nicknames: bool
    manage_roles: bool
    manage_threads: bool
    manage_webhooks: bool
    mention_everyone: bool
    moderate_members: bool
    move_members: bool
    mute_members: bool
    pin_messages: bool
    priority_speaker: bool
    read_message_history: bool
    request_to_speak: bool
    send_messages: bool
    send_messages_in_threads: bool
    send_polls: bool
    send_tts_messages: bool
    send_voice_messages: bool
    set_voice_channel_status: bool
    speak: bool
    start_embedded_activities: bool
    stream: bool
    use_external_apps: bool
    use_external_sounds: bool
    use_slash_commands: bool
    use_soundboard: bool
    use_voice_activation: bool
    view_audit_log: bool
    view_channel: bool
    view_creator_monetization_analytics: bool
    view_guild_insights: bool

def command[**P](
    name: str,
    description: str
) -> JDECommandDecorator[P]:
    """
    Create the base of a command.

    Args:
        name (str): Command name.
        description (str): Command description.

    Returns:
        JDECommandDecorator[P]: Command.
    """

def has_permissions[**P](
    **permissions: Unpack[JDEPermissionOptions]
) -> JDECommandDecorator[P]:
    """
    Allow command to be ran only by users having the specified permissions.

    Args:
        **permissions (Unpack[JDEPermissionOptions]): Command permissions.

    Returns:
        JDECommandDecorator[P]: Command.
    """

def bot_has_permissions[**P](
    **permissions: Unpack[JDEPermissionOptions]
) -> JDECommandDecorator[P]:
    """
    Allow command to be ran only if the bot have the specified permissions.

    Args:
        **permissions (Unpack[JDEPermissionOptions]): Command bot permissions.

    Returns:
        JDECommandDecorator: Command.
    """

def guild_only[**P]() -> JDECommandDecorator[P]:
    """
    Allow command to be ran only in guilds.

    Returns:
        JDECommandDecorator: Command.
    """

def is_owner[**P]() -> JDECommand[P]:
    """
    Allow command to be ran only by the owner.

    Returns:
        JDECommand[P]: Command.
    """

def checks[**P](
    *callbacks: JDECommand
) -> JDECommandDecorator[P]:
    """
    Allow command to be ran only if all custom conditions are checked.

    Args:
        *callbacks (JDECommand): Functions the check custom conditions.

    Returns:
        JDECommandDecorator[P]: Command.
    """

def option[**P](
    name: str,
    description: str,
    option_type: type[str | int | float | bool] | Literal["user", "channel", "role", "mentionable", "attachment"],
    required: bool = True,
    choices: list | tuple | None = None,
    min_value: int | float | None = None,  # noqa: PYI041
    max_value: int | float | None = None,  # noqa: PYI041
    min_length: int | float | None = None,  # noqa: PYI041
    max_length: int | float | None = None  # noqa: PYI041
) -> JDECommandDecorator[P]:
    """
    Add an option to the command.

    Args:
        name (str): Option name.
        description (str): Option description.
        option_type (type[str | int | float | bool] | Literal["user", "channel", "role", "mentionable", "attachment"]): Option type.
        required (bool): Whether the option is required.
        choices (list | tuple | None): List of choices for the option.
        min_value (int | float | None): Minimum value (if option is a int or float).
        max_value (int | float | None): Maximum value (if option is a int or float).
        min_length (int | float | None): Minimum length (if option is a str).
        max_length (int | float | None): Maximum length (if option is a str).

    Returns:
        JDECommandDecorator[P]: Command.
    """

def cooldown[**P](
    rate: int,
    per: int | float,  # noqa: PYI041
    scope: Literal["user", "guild", "channel", "global"] = "user"
) -> JDECommandDecorator[P]:
    """
    Add an option to the command.

    Args:
        rate (int): Maximum execution amount.
        per (str): Cooldown period.
        scope (Literal["user", "guild", "channel", "global"]): Cooldown scope.

    Returns:
        JDECommandDecorator[P]: Command.
    """

__all__: Sequence[str] = [
    "bot_has_permissions",
    "checks",
    "command",
    "cooldown",
    "guild_only",
    "has_permissions",
    "is_owner",
    "option"
]
