"""Config file handler"""

from collections.abc import Sequence
from typing import Any, Literal, final

from jardiscordengine.interns import JTKExternConfig
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import documented
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy,
)

CONFIGS: dict[str, JDEInternConfig]

@documented
@final
class JDEInternConfig(
    JTKExternConfig.Config,
    JDEInternBaseClass[
        Literal[JDEInternInstancePolicy.UNIQUE],
        Literal[0],
        Literal[False],
    ]
):

    project_path: str | None
    config_path: str | None
    state_path: str | None

    def __init__(
        self,
        name: str,
        data: dict[str, dict[str, Any]] | None = None,
        is_state: bool = False,
        *,
        metadata: dict[str, Any] | None = None,
        has_extension: bool = True,
    ) -> None:
        """
        Create/Open a config file.

        Args:
            name (str): Config file name.
            data (dict[str, dict[str, Any]] | None): Config default data.
            is_state (bool): Set the config file as a state report file.
            metadata (dict[str, Any] | None): Config file metadata.
            has_extension (bool): Append '.ini' to the file name.
        """

def get[
    TYPE: type
](
    name: str,
    section: str,
    setting: str,
    type: TYPE = str,
    default: TYPE | None = None
) -> TYPE:
    """
    Get a config setting.

    Args:
        name (str): Config name.
        section (str): Config section.
        setting (str): Config setting.
        type (@TYPE): Config setting's type.
        default (@TYPE | None): Default value on failure.

    Returns:
        @TYPE: Setting value.
    """

def set(
    name: str,
    section: str,
    setting: str,
    value: Any
) -> None:
    """
    Set a config setting.

    Args:
        name (str): Config name.
        section (str): Config section.
        setting (str): Config setting.
        value (Any): Config setting's value.
    """

def init_all(
) -> None:
    """Initialize all required config instances"""

def check_compatibility(
) -> None:
    """Check all config instances compatibility"""

__all__: Sequence[str] = [
    "CONFIGS",
    "JDEInternConfig",
    "check_compatibility",
    "get",
    "init_all",
    "set"
]
