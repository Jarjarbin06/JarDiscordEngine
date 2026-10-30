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

from datetime import UTC as _UTC
from datetime import datetime as _datetime
from urllib.parse import urlparse as _urlparse

import aiohttp as _aiohttp
import discord as _discord

from jardiscordengine.interns import JTKExternTime as _JTKExternTime
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import field as _field
from jardiscordengine.interns.decorators import flag as _flag
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.helpers import assert_is_instance as _assert_is_instance
from jardiscordengine.interns.high_classes import (
    JDEInternFieldURL as _JDEInternFieldURL,
)
from jardiscordengine.interns.low_classes import JDEInternEntity as _JDEInternEntity


def _is_http_url(value):
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    parsed = _urlparse(value)
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)

def _validate_optional_url(value, name):
    if value is not None and (not _is_http_url(value)):
        raise ValueError(f'{name} must be an absolute HTTP or HTTPS URL')

def _validate_text(value, name, maximum_length):
    if value is None:
        return
    if not isinstance(value, str):
        raise TypeError(f'{name} must be str or None')
    if len(value) > maximum_length:
        raise ValueError(f'{name} cannot exceed {maximum_length} characters')

def _validate_embed_fields(value):
    if not isinstance(value, list) or len(value) > 25:
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        name = item.get('name')
        field_value = item.get('value')
        inline = item.get('inline', False)
        if not isinstance(name, str) or not name:
            return False
        if not isinstance(field_value, str) or not field_value:
            return False
        if len(name) > 256 or len(field_value) > 1024:
            return False
        if not isinstance(inline, bool):
            return False
    return True

def _validate_message_embeds(value):
    if not isinstance(value, list) or len(value) > 10:
        return False
    return all(isinstance(embed, (JDEEntityWebhookEmbed, _discord.Embed)) for embed in value)

def _to_discord_embed(embed):
    if isinstance(embed, JDEEntityWebhookEmbed):
        return embed.to_discord_embed()
    if isinstance(embed, _discord.Embed):
        return embed
    raise TypeError('An embed must be JDEEntityWebhookEmbed or discord.Embed')

def _normalise_embeds(embeds):
    if len(embeds) > 10:
        raise ValueError('A Discord message cannot contain more than 10 embeds')
    return [_to_discord_embed(embed) for embed in embeds]

@_documented
class JDEEntityWebhookEmbed(_JDEInternEntity):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    title = _field((str, type(None)), default=None, validator=lambda value: value is None or len(value) <= 256, doc='Embed title, limited to 256 characters.')
    description = _field((str, type(None)), default=None, validator=lambda value: value is None or len(value) <= 4096, doc='Embed description, limited to 4096 characters.')
    url = _field((str, type(None)), default=None, validator=_is_http_url, doc='Optional URL associated with the embed title.')
    color = _field((int, type(None)), default=None, doc='Embed color represented as an RGB integer.')
    timestamp = _field((_datetime, type(None)), default=None, doc='Optional timestamp displayed by Discord.')
    author_name = _field((str, type(None)), default=None, validator=lambda value: value is None or len(value) <= 256, doc='Embed author name.')
    author_url = _field((str, type(None)), default=None, validator=_is_http_url, doc='Optional URL associated with the embed author.')
    author_icon_url = _field((str, type(None)), default=None, validator=_is_http_url, doc='Optional author icon URL.')
    footer_text = _field((str, type(None)), default=None, validator=lambda value: value is None or len(value) <= 2048, doc='Embed footer text.')
    footer_icon_url = _field((str, type(None)), default=None, validator=_is_http_url, doc='Optional footer icon URL.')
    image_url = _field((str, type(None)), default=None, validator=_is_http_url, doc="URL of the embed's main image.")
    thumbnail_url = _field((str, type(None)), default=None, validator=_is_http_url, doc="URL of the embed's thumbnail.")
    fields = _field(list, default=[], validator=_validate_embed_fields, doc='List of embed fields.')

    def __new__(cls, _jde_key = None, _jde_warn = None, **kwargs):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn
        )

    def __init__(self, title = None, description = None, color = None, url = None, timestamp = None):

        _JDEInternEntity.__init__(self)

        self.title = title
        self.description = description
        self.url = url

        if isinstance(timestamp, _JTKExternTime.Time):
            timestamp = _datetime.fromtimestamp(timestamp.timestamp(), _UTC)

        if isinstance(timestamp, _JTKExternTime.Time):
            timestamp = _datetime.fromtimestamp(timestamp.timestamp(), _UTC)

        elif isinstance(timestamp, (int, float)):
            timestamp = _datetime.fromtimestamp(timestamp, _UTC)

        self.timestamp = timestamp

        if color is not None:
            self.set_color(color)

    def set_title(self, title):
        _validate_text(title, 'title', 256)

        self.title = title

        return self

    def set_description(self, description):
        _validate_text(description, 'description', 4096)

        self.description = description

        return self

    def add_text(self, text, separator = '\n'):
        _assert_is_instance(text, str, 'TEXT must be str')
        _assert_is_instance(separator, str, 'SEPARATOR must be str')

        if self.description:
            description = self.description + separator + text  # pyright: ignore[reportOperatorIssue]

        else:
            description = text

        _validate_text(description, 'description', 4096)

        self.description = description

        return self

    def clear_text(self):
        self.description = None

        return self

    def set_url(self, url):
        _validate_optional_url(url, 'Embed URL')

        self.url = url

        return self

    def set_color(self, color):
        if color is None:
            self.color = None
            return self

        if isinstance(color, _discord.Colour):
            color_value = color.value

        elif hasattr(color, 'rgb'):
            rgb = color.rgb
            if not isinstance(rgb, (tuple, list)) or len(rgb) != 3:
                raise TypeError('JDEColor must expose an RGB tuple')
            color_value = (rgb[0] << 16) | (rgb[1] << 8) | rgb[2]

        elif isinstance(color, int):
            color_value = color

        elif isinstance(color, str):
            hex_value = color.removeprefix('#')

            if len(hex_value) != 6:
                raise ValueError('A hexadecimal embed color must contain 6 digits')

            try:
                color_value = int(hex_value, 16)
            except ValueError as exc:
                raise ValueError(f'Invalid hexadecimal color: {color!r}') from exc

        else:
            raise TypeError('Color must be int, str, discord.Colour, or None')

        if not 0 <= color_value <= 16777215:
            raise ValueError('Embed color must be between 0x000000 and 0xFFFFFF')

        self.color = color_value
        return self

    def set_timestamp(self, timestamp = None):
        if timestamp is None:
            timestamp = _JTKExternTime.Time()

        if isinstance(timestamp, _JTKExternTime.Time):
            timestamp = _datetime.fromtimestamp(timestamp.timestamp(), _UTC)

        elif isinstance(timestamp, (int, float)):
            timestamp = _datetime.fromtimestamp(timestamp, _UTC)

        if not isinstance(timestamp, _datetime):
            raise TypeError('Timestamp must be Time, datetime, numeric timestamp, or None')

        self.timestamp = timestamp

        return self

    def clear_timestamp(self):
        self.timestamp = None

        return self

    def set_author(self, name, url=None, icon_url=None):
        _validate_text(name, 'author name', 256)
        _validate_optional_url(url, 'Author URL')
        _validate_optional_url(icon_url, 'Author icon URL')

        if name is None:
            self.author_name = None
            self.author_url = None
            self.author_icon_url = None

            return self

        if not name:
            raise ValueError('Author name cannot be empty')

        self.author_name = name
        self.author_url = url
        self.author_icon_url = icon_url

        return self

    def clear_author(self):
        self.author_name = None
        self.author_url = None
        self.author_icon_url = None

        return self

    def set_footer(self, text, icon_url = None):
        _validate_text(text, 'footer text', 2048)
        _validate_optional_url(icon_url, 'Footer icon URL')

        if text is None:
            self.footer_text = None
            self.footer_icon_url = None

            return self

        if not text:
            raise ValueError('Footer text cannot be empty')

        self.footer_text = text
        self.footer_icon_url = icon_url

        return self

    def clear_footer(self):
        self.footer_text = None
        self.footer_icon_url = None

        return self

    def set_image(self, url):
        _validate_optional_url(url, 'Image URL')

        self.image_url = url

        return self

    def add_image(self, url):
        return self.set_image(url)

    def clear_image(self):
        self.image_url = None

        return self

    def set_thumbnail(self, url):
        _validate_optional_url(url, 'Thumbnail URL')

        self.thumbnail_url = url

        return self

    def add_thumbnail(self, url):
        return self.set_thumbnail(url)

    def clear_thumbnail(self):
        self.thumbnail_url = None

        return self

    def add_field(self, name, value, inline = False):
        _assert_is_instance(name, str, 'FIELD NAME must be str')
        _assert_is_instance(value, str, 'FIELD VALUE must be str')
        _assert_is_instance(inline, bool, 'INLINE must be bool')

        if not name:
            raise ValueError('Field name cannot be empty')

        if not value:
            raise ValueError('Field value cannot be empty')

        if len(name) > 256:
            raise ValueError('Field name cannot exceed 256 characters')

        if len(value) > 1024:
            raise ValueError('Field value cannot exceed 1024 characters')

        if len(self.fields) >= 25:  # pyright: ignore[reportArgumentType]
            raise ValueError('An embed cannot contain more than 25 fields')

        self.fields.append({'name': name, 'value': value, 'inline': inline})  # pyright: ignore[reportAttributeAccessIssue]

        return self

    def remove_field(self, index):
        _assert_is_instance(index, int, 'INDEX must be int')

        if not 0 <= index < len(self.fields):  # pyright: ignore[reportArgumentType]
            raise IndexError('Embed field index is out of range')

        self.fields.pop(index)  # pyright: ignore[reportAttributeAccessIssue]

        return self

    def clear_fields(self):
        self.fields.clear()  # pyright: ignore[reportAttributeAccessIssue]

        return self

    def to_discord_embed(self):
        embed = _discord.Embed(title=self.title, description=self.description, url=self.url, color=_discord.Colour(self.color) if self.color is not None else None, timestamp=self.timestamp)  # pyright: ignore[reportArgumentType]

        if self.author_name is not None:
            embed.set_author(name=self.author_name, url=self.author_url, icon_url=self.author_icon_url)

        if self.footer_text is not None:
            embed.set_footer(text=self.footer_text, icon_url=self.footer_icon_url)

        if self.image_url is not None:
            embed.set_image(url=self.image_url)

        if self.thumbnail_url is not None:
            embed.set_thumbnail(url=self.thumbnail_url)

        for item in self.fields:  # pyright: ignore[reportGeneralTypeIssues]
            embed.add_field(name=item['name'], value=item['value'], inline=item['inline'])

        text_length = len(embed.title or '') + len(embed.description or '') + len(embed.author.name or '' if embed.author else '') + len(embed.footer.text or '' if embed.footer else '') + sum(len(item['name']) + len(item['value']) for item in embed.fields)  # pyright: ignore[reportIndexIssue]

        if text_length > 6000:
            raise ValueError('The combined text in an embed cannot exceed 6000 characters')

        return embed

@_documented
class JDEEntityWebhookMessage(_JDEInternEntity):

    __instance_policy__ = _JDEInternInstancePolicy.NORMAL
    __instance_limit__ = 0
    __recursive__ = False

    content = _field((str, type(None)), default=None, validator=lambda value: value is None or len(value) <= 2000, doc='Message content, limited to 2000 characters.')
    embeds = _field(list, default=list, validator=_validate_message_embeds, doc='Embeds included in the message, up to 10.')
    username = _field((str, type(None)), default=None, doc='Optional username override for the webhook.')
    avatar_url = _field((str, type(None)), default=None, validator=_is_http_url, doc='Optional avatar URL override for the webhook.')
    tts = _field(bool, default=False, doc='Whether the message should use text-to-speech.')
    allowed_mentions = _field((_discord.AllowedMentions, type(None)), default=None, doc='Optional Discord allowed-mentions configuration.')
    file = _field(object, default=None, doc='Optional single file attachment.')
    files = _field(list, default=list, doc='Optional collection of file attachments.')
    view = _field(object, default=None, doc='Optional Discord UI view.')
    thread = _field(object, default=None, doc='Optional thread to which the message should be sent.')
    thread_name = _field((str, type(None)), default=None, doc='Optional name for a newly created thread.')
    suppress_embeds = _field(bool, default=False, doc='Whether embeds generated from message content should be suppressed.')
    silent = _field(bool, default=False, doc='Whether to suppress notification sounds.')
    delete_after = _field((int, float, type(None)), default=None, doc='Optional delay after which the message should be deleted.')

    def __new__(cls, _jde_key = None, _jde_warn = None, **kwargs):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn
        )

    def __init__(self, content = None, embeds = None, username = None, avatar_url = None, tts = False, allowed_mentions = None, file = None, files = None, view = None, thread = None, thread_name = None, suppress_embeds = False, silent = False, delete_after = None):

        _JDEInternEntity.__init__(self)

        self.content = content
        self.username = username
        self.avatar_url = avatar_url
        self.tts = tts
        self.allowed_mentions = allowed_mentions
        self.file = file
        self.files = list(files) if files is not None else []
        self.view = view
        self.thread = thread
        self.thread_name = thread_name
        self.suppress_embeds = suppress_embeds
        self.silent = silent
        self.delete_after = delete_after

        if embeds is None:
            self.embeds = []

        elif isinstance(embeds, JDEEntityWebhookEmbed | _discord.Embed):
            self.embeds = [embeds]

        else:
            self.embeds = list(embeds)

    def set_content(self, content):
        self.content = content
        return self

    def append_content(self, content, separator='\n'):
        _assert_is_instance(content, str, 'CONTENT must be str')
        _assert_is_instance(separator, str, 'SEPARATOR must be str')
        if self.content:
            self.content += separator + content
        else:
            self.content = content
        return self

    def add_embed(self, embed):
        if not isinstance(embed, JDEEntityWebhookEmbed | _discord.Embed):
            raise TypeError('Embed must be JDEEntityWebhookEmbed or discord.Embed')

        if len(self.embeds) >= 10:  # pyright: ignore[reportArgumentType]
            raise ValueError('A Discord message cannot contain more than 10 embeds')

        self.embeds.append(embed)  # pyright: ignore[reportAttributeAccessIssue]

        return self

    def clear_embeds(self):
        self.embeds.clear()  # pyright: ignore[reportAttributeAccessIssue]

        return self

    def set_username(self, username):
        self.username = username

        return self

    def set_avatar_url(self, avatar_url):
        _validate_optional_url(avatar_url, 'Avatar URL')

        self.avatar_url = avatar_url

        return self

    def to_kwargs(self):
        if self.content is None and (not self.embeds) and (self.file is None) and (not self.files):
            raise ValueError('A webhook message must contain content, an embed, or an attachment')

        payload = {}

        if self.content is not None:
            payload['content'] = self.content

        if self.embeds:
            payload['embeds'] = _normalise_embeds(self.embeds)

        if self.username is not None:
            payload['username'] = self.username

        if self.avatar_url is not None:
            payload['avatar_url'] = self.avatar_url

        payload['tts'] = self.tts

        if self.allowed_mentions is not None:
            payload['allowed_mentions'] = self.allowed_mentions

        if self.file is not None:
            payload['file'] = self.file

        if self.files:
            payload['files'] = self.files

        if self.view is not None:
            payload['view'] = self.view

        if self.thread is not None:
            payload['thread'] = self.thread

        if self.thread_name is not None:
            payload['thread_name'] = self.thread_name

        if self.suppress_embeds:
            payload['suppress_embeds'] = True

        if self.silent:
            payload['silent'] = True

        if self.delete_after is not None:
            payload['delete_after'] = self.delete_after

        return payload

@_documented
class JDEEntityWebhook(_JDEInternEntity, _JDEInternFieldURL):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    def __new__(cls, url, _jde_key = None, _jde_warn = None):
        return _JDEInternEntity.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else url,
            _jde_warn=_jde_warn if _jde_warn is not None else True
        )

    def __init__(self, url):

        _JDEInternEntity.__init__(self)
        _JDEInternFieldURL.__init__(self, url)

        _validate_optional_url(url, 'Webhook URL')

        self._last_response = None
        self._last_sent_at = None

    @_flag(name='_last_response', doc='The response from the most recent webhook send.')
    def last_response(self):
        return '_last_response'

    @_flag(name='_last_sent_at', doc='UTC timestamp of the most recent webhook send.')
    def last_sent_at(self):
        return '_last_sent_at'

    async def __call__(self, message=None, *, content=None, embed=None, embeds=None, **kwargs):
        payload = {}

        if isinstance(message, JDEEntityWebhookMessage):
            payload.update(message.to_kwargs())

        elif isinstance(message, str):
            payload['content'] = message

        elif isinstance(message, (JDEEntityWebhookEmbed, _discord.Embed)):
            payload['embeds'] = [_to_discord_embed(message)]

        elif message is not None:
            raise TypeError('message must be str, JDEEntityWebhookMessage, JDEEntityWebhookEmbed, discord.Embed, or None')

        if content is not None:
            payload['content'] = content

        if embed is not None:
            converted_embed = _to_discord_embed(embed)
            current_embeds = payload.get('embeds', [])

            if len(current_embeds) >= 10:
                raise ValueError('A Discord message cannot contain more than 10 embeds')

            payload['embeds'] = [*current_embeds, converted_embed]

        if embeds is not None:
            converted_embeds = _normalise_embeds(list(embeds))
            current_embeds = payload.get('embeds', [])

            if len(current_embeds) + len(converted_embeds) > 10:
                raise ValueError('A Discord message cannot contain more than 10 embeds')

            payload['embeds'] = [*current_embeds, *converted_embeds]

        payload.update(kwargs)

        if 'embed' in payload:
            native_embed = payload.pop('embed')
            current_embeds = payload.get('embeds', [])

            if native_embed is not None:
                if len(current_embeds) >= 10:
                    raise ValueError('A Discord message cannot contain more than 10 embeds')

                payload['embeds'] = [*current_embeds, _to_discord_embed(native_embed)]

        if 'embeds' in payload:
            payload['embeds'] = _normalise_embeds(list(payload['embeds']))

        payload.setdefault('wait', True)

        if payload.get('content') is None and (not payload.get('embeds')) and (payload.get('file') is None) and (not payload.get('files')):
            raise ValueError('A webhook message must contain content, an embed, or an attachment')

        if payload.get('content') is not None:
            _validate_text(payload['content'], 'content', 2000)

        if len(payload.get('embeds', [])) > 10:
            raise ValueError('A Discord message cannot contain more than 10 embeds')

        async with _aiohttp.ClientSession() as session:
            webhook = _discord.Webhook.from_url(self.url, session=session)  # pyright: ignore[reportArgumentType]
            response = await webhook.send(**payload)

        self._last_response = response
        self._last_sent_at = _datetime.now(_UTC)

        return response

    async def send(self, message=None, **kwargs):
        return await self(message, **kwargs)
