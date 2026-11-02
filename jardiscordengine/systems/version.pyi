from collections.abc import Sequence
from typing import final

from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.enums import JDEInternInstancePolicy
from jardiscordengine.systems.enums import JDECompatibility

@final
class JDEVersion(
    JDEInternBaseClass[
        JDEInternInstancePolicy.NORMAL,
        0,
        False,
    ]
):
    """
    Version data.

    Attributes:
        major (int): Major version.
        minor (int): Minor version.
        patch (int): Patch version.
    """

    major: int
    minor: int
    patch: int

    def __init__(
        self,
        major: int,
        minor: int,
        patch: int,
    ) -> None:
        """
        Initialize a version

        Args:
            major (int): Major version
            minor (int): Minor version
            patch (int): Patch version
        """

    def compatibility(
        self,
        other: JDEVersion,
    ) -> JDECompatibility:
        """
        Check if current version is compatible with an other.

        - JDECompatibility.ERROR - Different major / Old minor.
        - JDECompatibility.WARNING - New minor / New patch.
        - JDECompatibility.OK - Same version.

        Args:
            other (JDEVersion): Version to compare to.

        Returns:
            JDECompatibility: Compatibility status.
        """

__all__: Sequence[str] = [
    "JDEVersion",
]
