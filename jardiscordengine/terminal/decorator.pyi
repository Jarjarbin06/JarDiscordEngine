from collections.abc import Awaitable, Callable

type JDECommand = Callable[[list[str]], Awaitable[None]]
type JDECommandDecorator = Callable[[JDECommand], JDECommand]

def terminal_command(
    name: str,
    description: str,
    *arguments: tuple[str, str],
) -> JDECommandDecorator:
    """
    Make the function a JDETerminal command.

    Args:
        name (str): Command name.
        description (str): Command description.
        *arguments (tuple[str, str]): Command arguments (name, description).

    Returns:
        JDECommandDecorator: JDETerminal command.
    """
