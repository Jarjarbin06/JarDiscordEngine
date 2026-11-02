from collections.abc import Awaitable, Callable

def terminal_command(
    name: str,
    description: str,
    *arguments: tuple[str, str],
) -> Callable[[Callable[[list[str]], Awaitable[None]]], Callable[[list[str]], Awaitable[None]]]:
    """
    Make the function a JDETerminal command.

    Args:
        name (str): Command name.
        description (str): Command description.
        *arguments (tuple[str, str]): Command arguments (name, description).

    Returns:
        Callable[[Callable[[list[str]], Awaitable[None]]], Callable[[list[str]], Awaitable[None]]]: JDETerminal command.
    """
