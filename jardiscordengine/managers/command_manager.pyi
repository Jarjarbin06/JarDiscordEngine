from collections.abc import Awaitable, Callable, Sequence
from typing import Concatenate, final

from jardiscordengine.bots.bot import JDEBot
from jardiscordengine.entities.commands import (
    JDEEntityApplicationContext,
)
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass,
)
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)

type JDECommand[**P] = Callable[Concatenate[JDEBot, JDEEntityApplicationContext, P], Awaitable[None]]

@final
class JDECommandManager(
    JDEInternBaseClass[
        JDEInternInstancePolicy.SINGLETON,
        1,
        True,
    ]
):

    def __init__(
        self,
        bot: JDEBot
    ) -> None:
        """
        Create a command manager.

        Args:
            bot (JDEBot): Bot that will handle commands.
        """

    @property
    def bot(
        self
    ) -> JDEBot:
        """
        Get the linked bot.

        Returns:
            JDEBot: Bot.
        """

    @property
    def commands(
        self
    ) -> dict[str, JDECommand[...]]:
        """
        Get the registered commands.

        Returns:
            dict[str, JDECommand[...]]: Commands.
        """

    def register_command[**P](
        self,
        callback: JDECommand[P]
    ) -> None:
        """
        Register a command to the manager.

        Args:
            callback (JDECommand[P]): Command.
        """

    def register_commands(
        self,
        *callbacks: JDECommand[...]
    ) -> None:
        """
        Register commands to the manager in batch.

        Args:
            *callbacks (JDECommand[...]): Commands.
        """

    def get_command(
        self,
        name: str
    ) -> JDECommand[...]:
        """
        Get a command by it's name.

        Args:
            name (str): Command name.

        Returns:
            JDECommand[...]: Command.
        """

    def unregister_command(
        self,
        name: str
    ) -> JDECommand[...]:
        """
        Unregister a command.

        Args:
            name (str): Command name.

        Returns:
            JDECommand[...]: Unregistered command.
        """

__all__: Sequence[str] = [
    "JDECommandManager",
]
