from collections.abc import Awaitable, Callable
from typing import Literal, final

from jardiscordengine.bots.bot import JDEBot
from jardiscordengine.interns import JTKExternError
from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.decorators import documented, logged, timed
from jardiscordengine.interns.enums import JDEInternInstancePolicy

class JDETerminalRestart(JTKExternError.JErrorSystem):
    """Raise to the JarDiscordEngine a restart signal/exception"""

@final
@logged
@documented
class JDETerminal(
    JDEInternBaseClass[
        Literal[JDEInternInstancePolicy.SINGLETON],
        Literal[1],
        Literal[True],
    ]
):
    """Terminal handler."""

    def __init__(
        self,
        bot: JDEBot,
        prompt: str | None = None,
        on_ready: Callable[[], Awaitable[None]] | None = None
    ) -> None:
        """
        Create a terminal.

        Args:
            bot (JDEBot): Bot.
            prompt (str | None): Terminal command prompt.
            on_ready (Callable[[], Coroutine[Any, Any, None]] | None): Function that will be called when terminal AND bot ready.
        """

    @property
    def bot(
        self
    ) -> JDEBot:
        """
        Get linked bot.

        Returns:
            JDEBot: Bot linked to the terminal.
        """

    @property
    def commands(
        self
    ) -> dict[str, Callable[[list[str]], Awaitable[None]]]:
        """
        Get registered commands.

        Returns:
            dict[str, Callable[[list[str]], Awaitable[None]]]: Commands.
        """

    def register_command(
        self,
        handler: Callable[[list[str]], Awaitable[None]]
    ) -> None:
        """
        Register a terminal command.

        Args:
            handler (Callable[[list[str]], Awaitable[None]]): Command handler.
        """

    @timed
    async def run(
        self
    ) -> None:
        """Run the terminal interface."""
