from collections.abc import Sequence
from enum import IntEnum
from typing import final

@final
class JDECompatibility(IntEnum):
    """
    Version compatibility status.

    Attributes:
        OK (int): Version compatible.
        WARNING (int): Version compatible but needs an update.
        ERROR (int): Version incompatible.
    """

    OK: int
    WARNING: int
    ERROR: int

__all__: Sequence[str] = [
    "JDECompatibility",
]
