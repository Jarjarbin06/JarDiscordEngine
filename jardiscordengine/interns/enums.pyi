from collections.abc import Sequence
from enum import IntEnum
from typing import final

@final
class JDEInternInstancePolicy(IntEnum):
    """
    Instance policy.

    Attributes:
        NORMAL (int): Unlimited and unfiltered instantiation.
        SINGLETON (int): Only 1 instance.
        FLYWEIGHT (int): Limited instance amount.
        UNIQUE (int): Filtered instantiation.
    """

    NORMAL: JDEInternInstancePolicy
    SINGLETON: JDEInternInstancePolicy
    FLYWEIGHT: JDEInternInstancePolicy
    UNIQUE: JDEInternInstancePolicy

__all__: Sequence[str] = [
    "JDEInternInstancePolicy",
]
