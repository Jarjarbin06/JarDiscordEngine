from collections.abc import Sequence
from typing import Any, final

from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.enums import JDEInternInstancePolicy

@final
class JDEBool(
    JDEInternBaseClass[
        JDEInternInstancePolicy.FLYWEIGHT,
        2,
        False,
    ]
):
    """Boolean."""

    def __init__(
        self,
        value: Any,
    ) -> None:
        """
        Get boolean from a value.

        Args:
            value (Any): Value to to transform.
        """

__all__: Sequence[str] = [
    "JDEBool",
]
