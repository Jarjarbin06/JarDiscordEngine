from collections.abc import Sequence
from typing import Any, Self

from jardiscordengine.interns.decorators import documentation
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)

@documentation
class JDEInternBaseClass[
    PolicyT: JDEInternInstancePolicy,
    LimitT: int,
    RecursiveT: bool
]:
    """
    Internal base class that every JDE inherit from.

    Attributes:
        jdeid (str): JarDiscordEngine ID (unique object identifier)(UUID)
    """

    __instance_policy__: PolicyT
    __instance_limit__: LimitT
    __recursive__:RecursiveT

    jdeid: str

    def __new__(
        cls,
        *args: Any,
        **kwargs: Any,
    ) -> Self:
        """
        Create a new JDE object.

        Args:
            *args (Any): Arguments.
            **kwargs (Any): Key word arguments.

        Returns:
            Self: New instance.
        """

    def __init__(
        self,
    ) -> None:
        """Initialize a JDE object."""

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Get the dictionary of all public fields and functions of the JDE object.

        Returns:
            dict[str, Any]: Public features.
        """

    def debug(
        self,
        *,
        is_colored: bool = False,
        max_depth: int = -1,
        branched_recursive: bool = False,
        show_root: bool = True,
    ) -> str:
        """
        Get a debug representation of the JDE object.

        Args:
            is_colored (bool): Use colors for pretty printing.
            max_depth (int): Maximum exploration depth.
            branched_recursive (bool): Don't take in count the branches when exploring (allows an object to appear multiple times in debug mode).
            show_root (bool): Show the root JDE object.

        Returns:
            str: Debug string.
        """

__all__: Sequence[str] = [
    "JDEInternBaseClass",
]
