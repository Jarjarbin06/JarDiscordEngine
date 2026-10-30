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
import shlex as _shlex
from contextlib import suppress as _suppress
from typing import final as _final

from jardiscordengine.interns import JTKExternConsole as _JTKExternConsole
from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns import JTKExternTime as _JTKExternTime
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass as _JDEInternBaseClass,
)
from jardiscordengine.interns.config import get as _get
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import flag as _flag
from jardiscordengine.interns.decorators import logged as _logged
from jardiscordengine.interns.decorators import timed as _timed
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)
from jardiscordengine.interns.log import log as _log
from jardiscordengine.interns.log import save as _save
from jardiscordengine.terminal.decorator import terminal_command as _terminal_command


class JDETerminalRestart(_JTKExternError.JErrorSystem):
    pass

@_final
@_logged
@_documented
class JDETerminal(_JDEInternBaseClass):

    __instance_policy__ = _JDEInternInstancePolicy.SINGLETON
    __instance_limit__ = 1
    __recursive__ = True

    def __new__(cls, bot, prompt = None, _jde_key = None, _jde_warn = None, **kwargs):
        return _JDEInternBaseClass.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, bot, prompt = None, on_ready = None):
        if prompt is None:
            prompt = f"[JDE: {_get("project", "PROJECT", "name", str, "Unnamed project")}] > "

        self._bot = bot
        self._prompt = prompt
        self._running = False
        self._on_ready = on_ready
        self._restart_requested = False
        self._save_interval = _get("settings", "LOG", "save_per", int, 60)

        self._commands = {}
        self._description = {}
        self._arguments = {}

        self.register_command(self._command_exit)
        self.register_command(self._command_help)
        self.register_command(self._command_restart)

    def register_command(self, handler):
        name = getattr(handler, "cmd_name", handler.__name__)
        description = getattr(handler, "cmd_description", "No description")
        arguments = getattr(handler, "cmd_arguments", ())

        self._commands[name] = handler
        self._description[name] = description
        self._arguments[name] = arguments

    @_flag(doc="Bots")
    def bot(self):
        return "_bot"

    @_flag(doc="Commands")
    def commands(self):
        return "_commands"

    @_timed
    async def run(self):
        if self._running:
            raise RuntimeError("The runtime is already running.")

        self._running = True

        bot_task = _asyncio.create_task(
            self._bot._start(),
            name="jde-discord-bot",
        )

        ready_task = _asyncio.create_task(
            self._wait_until_ready(),
            name="jde-discord-ready",
        )

        save_task = _asyncio.create_task(
            self._periodic_log_save(),
            name="jde-periodic-log-save",
        )

        terminal_task = None
        startup_error = None

        try:
            try:
                await self._wait_for_bot(
                    bot_task,
                    ready_task,
                )
            except Exception as error:  # noqa: BLE001
                startup_error = error

            if startup_error is None and self._on_ready is not None:
                try:
                    await self._on_ready()
                except Exception as error:  # noqa: BLE001
                    startup_error = error

            if startup_error is None:
                terminal_task = _asyncio.create_task(
                    self._terminal_loop(),
                    name="jde-terminal-loop",
                )

                done, _ = await _asyncio.wait(
                    {bot_task, terminal_task},
                    return_when=_asyncio.FIRST_COMPLETED,
                )

                if bot_task in done:
                    await bot_task

        finally:
            self._running = False

            await self._cancel_task(save_task)
            await self._cancel_task(terminal_task)
            await self._cancel_task(ready_task)

            await self._stop_bot(bot_task)

            if startup_error is not None:
                _JTKExternConsole.print(
                    _JTKExternConsole.Text(
                        f"Startup failed: {startup_error}"
                    ).f_color_error()
                )

            if self._restart_requested:
                raise JDETerminalRestart("Restarting")

    async def _periodic_log_save(self):
        while self._running:
            await _asyncio.sleep(self._save_interval)

            if not self._running:
                break

            try:
                _save()
            except Exception as error:  # noqa: BLE001
                _JTKExternConsole.print(
                    self._color(
                        f"Failed to save logs: {error}",
                        255,
                        100,
                        100,
                    )
                )

    @staticmethod
    def _text(message):
        return _JTKExternConsole.Text(message)

    @staticmethod
    def _color(message, red, green, blue):
        return _JTKExternConsole.Text(message).f_color_foreground(_JTKExternConsole.ColorRGB(red, green, blue))

    @classmethod
    def _panel(cls, title, content):
        Text = _JTKExternConsole.Text

        heading = cls._color(title, 70, 160, 255)

        return Text(f"{heading}\n{content}").f_border_box(border=_JTKExternConsole.PresetBorder.ROUND, padding=1)

    async def _terminal_loop(self):

        _JTKExternConsole.print(self._panel("JAR DISCORD ENGINE", (
            f"{self._color(f'{len(self._commands)} commands registered', 180, 180, 180)}\n"
            f"{self._color('Terminal ready', 100, 220, 130)}\n"
            f"{self._color('Type help to list available commands.', 180, 180, 180)}\n"
            f"{self._color('Type exit to shut down.', 180, 180, 180)}"
        )))

        while self._running:
            try:
                prompt = self._color(self._prompt, 70, 160, 255)
                raw_command = await _asyncio.to_thread(input, prompt)
            except EOFError:
                _JTKExternConsole.print(self._color("\nEnd of terminal input.", 150, 150, 150))
                break

            try:
                arguments = _shlex.split(raw_command)
            except ValueError as error:
                _JTKExternConsole.print(self._color(f"Invalid command syntax: {error}", 255, 100, 100))
                continue

            if not arguments:
                continue

            command_name = arguments[0].lower()
            command_arguments = arguments[1:]

            handler = self._commands.get(command_name)

            if handler is None:
                _JTKExternConsole.print(self._color(f"Unknown command: {command_name}", 255, 100, 100))
                _log("WARN", "Terminal", f"Unknown command: {command_name}")
                continue

            try:
                await handler(command_arguments)
                _log("NOTICE", "Terminal", f"Command ran: {command_name}")

            except Exception as error:  # noqa: BLE001
                _JTKExternConsole.print(self._color(f"Command failed: {error}", 255, 100, 100))
                _log("ERROR", "Terminal", f"Command failed: {command_name} - {error}",)

    @_terminal_command(
        "exit",
        "Stop the bot and exit the terminal prompt.",
    )
    async def _command_exit(self, arguments):
        _JTKExternConsole.print(self._panel("SHUTTING DOWN", self._color("Stopping JarDiscordEngine...", 255, 180, 80)))
        self._running = False

    @_terminal_command(
        "help",
        "Display help information about terminal commands.",
        ("[command]", "Name of the command to get detailed help for."),
    )
    async def _command_help(self, arguments):
        if not arguments:
            self._show_general_help()
            return

        name = arguments[0].lower()

        if name not in self._commands:
            _JTKExternConsole.print(self._color(f"Unknown command: {name}", 255, 100, 100))
            return

        self._show_command_help(name)

    @_terminal_command(
        "restart",
        "Restart the entire application.",
    )
    async def _command_restart(self, arguments):
        _JTKExternConsole.print(
            self._panel(
                "RESTARTING",
                self._color(
                    "Stopping JarDiscordEngine before restarting...",
                    255,
                    180,
                    80,
                ),
            )
        )

        self._restart_requested = True
        self._running = False

    def _show_general_help(self):
        Text = _JTKExternConsole.Text

        lines = [self._color("Available commands", 200, 200, 200), ""]

        for name in sorted(self._commands):
            command_arguments = self._arguments[name]
            argument_names = []

            for argument_name, _ in command_arguments:
                if (
                    argument_name.startswith("[")
                    and argument_name.endswith("]")
                ):
                    argument_names.append(argument_name)
                else:
                    argument_names.append(f"<{argument_name}>")

            usage = name

            if argument_names:
                usage += " " + " ".join(argument_names)

            usage_text = self._color(Text(f"{usage:<34}").f_layout_indent(1), 70, 160, 255)
            description_text = self._text(self._description[name])

            lines.append(f"{usage_text}{description_text}")

        lines.extend(["", self._color("Use 'help <command>' for detailed information.", 150, 150, 150)])

        _JTKExternConsole.print(Text("\n".join(lines)).f_border_box(border=_JTKExternConsole.PresetBorder.ROUND, padding=1))

    def _show_command_help(self, name):
        Text = _JTKExternConsole.Text

        description = self._description[name]
        command_arguments = self._arguments[name]

        heading = self._color(f"Command: {name}", 70, 160, 255)

        lines = [heading, "", self._color("DESCRIPTION", 200, 200, 200), Text(description).f_layout_indent(1), "", self._color("USAGE", 200, 200, 200)]

        usage = name

        for argument_name, _ in command_arguments:
            if (
                argument_name.startswith("[")
                and argument_name.endswith("]")
            ):
                usage += f" {argument_name}"
            else:
                usage += f" <{argument_name}>"

        lines.append(Text(usage).f_layout_indent(1))

        if command_arguments:
            lines.extend(["", self._color("ARGUMENTS", 200, 200, 200)])

            for argument_name, argument_description in command_arguments:
                lines.append(Text(self._color(argument_name, 70, 160, 255)).f_layout_indent(1))
                lines.append(Text(argument_description).f_layout_indent(2))
        else:
            lines.extend(["", self._color("This command takes no arguments.", 150, 150, 150)])

        _JTKExternConsole.print(Text("\n".join(lines)).f_border_box(border=_JTKExternConsole.PresetBorder.ROUND, padding=1))

    async def _wait_until_ready(self):
        while True:
            try:
                await self._bot.discord.wait_until_ready()
            except RuntimeError:
                await _asyncio.sleep(0.05)
            else:
                return

    @staticmethod
    async def _cancel_task(task):
        if task is None or task.done():
            return

        task.cancel()

        with _suppress(_asyncio.CancelledError):
            await task

    async def _stop_bot(self, bot_task):
        discord_bot = self._bot.discord

        if not bot_task.done():
            if discord_bot.is_ready():
                await self._bot._stop()
            else:
                bot_task.cancel()

            try:
                await bot_task
            except _asyncio.CancelledError:
                pass
            except Exception as error:  # noqa: BLE001
                if isinstance(error, RuntimeError) and str(error) == "Session is closed":
                    _JTKExternConsole.print("\n" + _JTKExternConsole.Text("Disconnected from Discord").f_color_green() + "\n")
                else:
                    _JTKExternConsole.print("\n" + _JTKExternConsole.Text(f"Bot stopped with an error: {error}").f_color_error() + "\n")

        if not discord_bot.is_closed():
            await self._bot._stop()

    async def _wait_for_bot(self, bot_task, ready_task):
        animation = _JTKExternConsole.Animation.Spinner.braille(
            duration=0.1,
        )

        status = "Connecting to Discord"

        renderer = _JTKExternConsole.Animation.AnimationRenderer(
            render=lambda frame: _JTKExternConsole.print(
                _JTKExternConsole.ANSI.Cursor.CursorPosition.previous_line()
                + _JTKExternConsole.Text(
                    f"{status} {frame}"
                ).f_color_yellow(),
                flush=True,
            ),
            start=lambda: _JTKExternConsole.print(""),
            stop=lambda: _JTKExternConsole.print(
                _JTKExternConsole.ANSI.Cursor.CursorPosition.previous_line()
                + _JTKExternConsole.ANSI.Screen.ScreenErase.erase_line(),
                end="",
            ),
        )

        previous_time = _JTKExternTime.Time.tick()
        synchronization_started = False

        with renderer:
            renderer.render(animation.current)

            while True:
                if bot_task.done():
                    await bot_task

                    raise RuntimeError(
                        "The Discord bot stopped during startup."
                    )

                if ready_task.done():
                    await ready_task

                    if not synchronization_started:
                        synchronization_started = True
                        status = "Synchronizing Discord entities"

                if synchronization_started:
                    synchronization_event = (
                        self._bot._synchronization_event
                    )

                    if synchronization_event.is_set():
                        await self._bot._wait_until_synchronized()
                        break

                await _asyncio.sleep(0.05)

                current_time = _JTKExternTime.Time.tick()
                elapsed = current_time - previous_time
                previous_time = current_time

                animation.update(elapsed)
                renderer.render(animation.current)

        _JTKExternConsole.print(
            _JTKExternConsole.Text(
                "Discord connected and entities synchronized."
            ).f_color_green()
        )
        _JTKExternConsole.print("")
