from typing import Literal

from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import documented
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)

@documented
class JDEInternEntity(
    JDEInternBaseClass
):
    """Entity (used for typing mostly)."""

    def __init__(
        self
    ) -> None:
        """Initialize an entity."""

@documented
class JDEInternField(
    JDEInternBaseClass
):
    """Field (used for typing mostly)."""

    def __init__(self):
        """Initialize a field."""
