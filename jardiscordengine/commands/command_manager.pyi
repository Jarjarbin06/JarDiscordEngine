from collections.abc import Awaitable, Callable, Sequence
from typing import Literal, final

from jardiscordengine.bots.bot import JDEBot
from jardiscordengine.entities.commands import (
    JDEEntityApplicationContext,
)
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import (
    documented,
    logged,
    register_entity,
    requires_init,
)
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)

@final
@logged
@documented
@register_entity(name="JDECommandManager", category="Manager")
class JDECommandManager(
    JDEInternBaseClass[
        Literal[JDEInternInstancePolicy.SINGLETON],
        Literal[1],
        Literal[True],
    ]
):

    @requires_init
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
    ) -> dict[str, Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]]:
        """
        Get the registered commands.

        Returns:
            dict[str, Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]]: Commands.
        """

    def register_command(
        self,
        callback: Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]
    ) -> None:
        """
        Register a command to the manager.

        Args:
            callback (Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]): Command.
        """

    def register_commands(
        self,
        *callbacks: Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]
    ) -> None:
        """
        Register commands to the manager in batch.

        Args:
            *callbacks (Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]): Commands.
        """

    def get_command(
        self,
        name: str
    ) -> Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]:
        """
        Get a command by it's name.

        Args:
            name (str): Command name.

        Returns:
            Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]: Command.
        """

    def unregister_command(
        self,
        name: str
    ) -> Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]:
        """
        Unregister a command.

        Args:
            name (str): Command name.

        Returns:
            Callable[[JDEBot, JDEEntityApplicationContext], Awaitable[None]]: Unregistered command.
        """

__all__: Sequence[str] = [
    "JDECommandManager",
]
