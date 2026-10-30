from collections.abc import Sequence
from typing import Any, Self

from jardiscordengine.interns.debug import JDEDebug
from jardiscordengine.interns.decorators import documented
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)

@documented
class JDEInternBaseClass[
    PolicyT: JDEInternInstancePolicy,
    LimitT: int,
    RecursiveT: bool
](JDEDebug):
    """
    Internal base class that every JDE inherit from.

    Attributes:
        jdeid (str): JarDiscordEngine ID (unique object identifier)(UUID)
    """

    __instance_policy__: PolicyT
    __instance_limit__: LimitT
    __recursive__: RecursiveT

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

__all__: Sequence[str] = [
    "JDEInternBaseClass",
]
