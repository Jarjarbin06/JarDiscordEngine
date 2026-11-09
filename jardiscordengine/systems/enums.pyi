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

    OK: ...
    WARNING: ...
    ERROR: ...

__all__: Sequence[str] = [
    "JDECompatibility",
]
