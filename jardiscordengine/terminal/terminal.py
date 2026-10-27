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

import asyncio
import shlex
from collections.abc import Awaitable, Callable
from contextlib import suppress
from typing import final as _final

from jardiscordengine.interns import JTKExternConsole as _JTKExternConsole
from jardiscordengine.interns import JTKExternTime as _JTKExternTime
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass as _JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import logged as _logged
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)

JDECommandHandler = Callable[[list[str]], Awaitable[None]]

@_final
@_logged
@_documented
class JDETerminal(_JDEInternBaseClass):

    __instance_policy__ = _JDEInternInstancePolicy.SINGLETON
    __instance_limit__ = 1
    __recursive__ = False

    def __new__(cls, bot, prompt = "JDE> ", _jde_key = None, _jde_warn = None, **kwargs):
        return _JDEInternBaseClass.__new__(
            cls,
            _jde_key=_jde_key,
            _jde_warn=_jde_warn if _jde_warn is not None else True,
        )

    def __init__(self, bot, prompt = "JDE> ", on_ready = None):
        self._bot = bot
        self._prompt = prompt
        self._running = False
        self._on_ready = on_ready
        self._commands: dict[str, JDECommandHandler] = {}

        self.register_command(
            "exit",
            self._command_exit,
        )

    def register_command(self, name, handler):
        self._commands[name] = handler

    async def run(self):
        if self._running:
            raise RuntimeError("The runtime is already running.")

        self._running = True

        bot_task = asyncio.create_task(
            self._bot.start(),
            name="jde-discord-bot",
        )

        ready_task = asyncio.create_task(
            self._wait_until_ready(),
            name="jde-discord-ready",
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
                terminal_task = asyncio.create_task(
                    self._terminal_loop(),
                    name="jde-terminal-loop",
                )

                done, _ = await asyncio.wait(
                    {bot_task, terminal_task},
                    return_when=asyncio.FIRST_COMPLETED,
                )

                if bot_task in done:
                    await bot_task

        finally:
            self._running = False

            await self._cancel_task(terminal_task)
            await self._cancel_task(ready_task)
            await self._stop_bot(bot_task)

            if startup_error is not None:
                _JTKExternConsole.print(
                    _JTKExternConsole.Text(
                        f"Startup failed: {startup_error}"
                    ).f_color_error()
                )

    async def _terminal_loop(self):
        while self._running:
            try:
                raw_command = await asyncio.to_thread(
                    input,
                    _JTKExternConsole.Text(self._prompt).f_color_foreground(_JTKExternConsole.ColorRGB(70, 160, 255)),
                )
            except EOFError:
                break

            try:
                arguments = shlex.split(raw_command)
            except ValueError as error:
                print(f"Invalid command syntax: {error}")
                continue

            if not arguments:
                continue

            command_name = arguments[0].lower()
            command_arguments = arguments[1:]

            handler = self._commands.get(command_name)

            if handler is None:
                print(f"Unknown command: {command_name}")
                continue

            try:
                await handler(command_arguments)
            except Exception as error:  # noqa: BLE001
                print(f"Command failed: {error}")

    async def _command_exit(self, arguments):
        self._running = False

    async def _wait_until_ready(self):
        while True:
            try:
                await self._bot.discord.wait_until_ready()
            except RuntimeError:
                await asyncio.sleep(0.05)
            else:
                return

    @staticmethod
    async def _cancel_task(task):
        if task is None or task.done():
            return

        task.cancel()

        with suppress(asyncio.CancelledError):
            await task

    async def _stop_bot(self, bot_task):
        discord_bot = self._bot.discord

        if not bot_task.done():
            if discord_bot.is_ready():
                await self._bot.close()
            else:
                bot_task.cancel()

            try:
                await bot_task
            except asyncio.CancelledError:
                pass
            except Exception as error:  # noqa: BLE001
                if isinstance(error, RuntimeError) and str(error) == "Session is closed":
                    _JTKExternConsole.print("\n" + _JTKExternConsole.Text("Disconnected from Discord").f_color_green() + "\n")
                else:
                    _JTKExternConsole.print("\n" + _JTKExternConsole.Text(f"Bot stopped with an error: {error}").f_color_error() + "\n")

        if not discord_bot.is_closed():
            await self._bot.close()

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
                        await self._bot.wait_until_synchronized()
                        break

                await asyncio.sleep(0.05)

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
