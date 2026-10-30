##Metadata##
__author__: str
__email__: str
__version__: str
__config_version__: str
__license__: str

##Imports##
from collections.abc import Awaitable, Callable

from . import bots as Bots
from . import commands as Commands
from . import entities as Entities
from . import events as Events
from . import interns as Interns
from . import systems as Systems
from . import terminal as Terminals
from .constants import *

##Lifetime##
def init(
    project_path: str
) -> None:
    """
    Initialize engine and its internal components.

    Args:
        project_path (str): Path to project root.
    """

@Interns.Decorators.requires_init
def quit() -> None:
    """Quit/uninitialize the engine."""

@Interns.Decorators.requires_init
@Interns.Decorators.handle_errors
def run(
    main: Callable[[], Awaitable[None]]
) -> None:
    """
    Run a main within engine handling capacity.

    Args:
        main (Callable[[], None]): Main to run.
    """

__all__ = [  # noqa: RUF022
    ## Special ##
    "__author__",
    "__email__",
    "__version__",
    "__license__",
    ## Imports ##
    "Bots",
    "Commands",
    "Entities",
    "Events",
    "Interns",
    "Systems",
    "Terminals",
    ## Constants ##
    # Versions #
    "JDEVersion_JarDiscordEngine",
    "JDEVersion_Config",
    "JDEVersion_Discord",
    "JDEVersion_Python",
    # Booleans #
    "JDEFalse",
    "JDETrue",
    ## Lifetime ##
    "init",
    "run",
    "quit",
]
