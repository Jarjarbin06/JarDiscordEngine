"""
JarDiscordEngine - Systems

Engine systems and non discord related components.
"""

from .bool import JDEBool as JDEBool
from .color import JDEColor as JDEColor
from .enums import (
    JDECompatibility as JDECompatibility,
)
from .version import JDEVersion as JDEVersion

__all__ = [
    'JDEBool',
    'JDEColor',
    'JDECompatibility',
    'JDEVersion',
]
