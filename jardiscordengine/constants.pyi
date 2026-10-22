from collections.abc import Sequence

from jardiscordengine.systems.bool import JDEBool
from jardiscordengine.systems.version import JDEVersion

# Versions #
JDEVersion_JarDiscordEngine: JDEVersion
JDEVersion_Config: JDEVersion
JDEVersion_Discord: JDEVersion
JDEVersion_Python: JDEVersion

# Booleans #
JDEFalse: JDEBool
JDETrue: JDEBool

__all__: Sequence[str] = [
    # Versions #
    "JDEVersion_JarDiscordEngine",
    "JDEVersion_Config",
    "JDEVersion_Discord",
    "JDEVersion_Python",
    # Booleans #
    "JDEFalse",
    "JDETrue"
]
