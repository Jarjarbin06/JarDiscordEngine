from collections.abc import Callable

def terminal_command(
    name: str,
    description: str,
    *arguments: tuple[str, str],
) -> Callable:
    """
    Make the function a JDETerminal command.

    Args:
        name (str): Command name.
        description (str): Command description.
        *arguments (tuple[str, str]): Command arguments (name, description).

    Returns:
        Callable: JDETerminal command.
    """
