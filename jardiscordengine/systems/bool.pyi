from collections.abc import Sequence
from typing import Any, Literal, final

from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.decorators import documentation
from jardiscordengine.interns.enums import JDEInternInstancePolicy

@documentation
@final
class JDEBool(
    JDEInternBaseClass[
        Literal[JDEInternInstancePolicy.FLYWEIGHT],
        Literal[2],
        Literal[False],
    ]
):
    """
    Boolean.

    Attributes:
        b (bool): Actual boolean.
    """

    b: bool

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
