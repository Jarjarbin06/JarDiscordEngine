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

    NORMAL: int
    SINGLETON: int
    FLYWEIGHT: int
    UNIQUE: int
