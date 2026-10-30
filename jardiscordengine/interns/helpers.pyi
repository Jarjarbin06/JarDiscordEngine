from collections.abc import Callable, Sequence

from jardiscordengine.interns import JTKExternError
from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.decorators import (
    requires_init,
)
from jardiscordengine.systems.version import JDEVersion

HAS_CRITICAL : bool = False

def assert_is_instance(
    obj: object,
    cls: type,
    msg: str | None = None
) -> None:
    """
    Raise exception if the object is not an instance of the given class.

    Args:
        obj (object): Object.
        cls (type): Class.
        msg (str | None): Error message.
    """

def deprecated(
    func: Callable,
    new_func: Callable,
    version: str | JDEVersion | None = None
) -> None:
    """
    Print a deprecated message.

    Args:
        func (Callable): Old/deprecated function.
        new_func (Callable): New function.
        version (str | JDEVersion | None): Version from which the version is deprecated.
    """

def critical(
    err: BaseException | JTKExternError.BaseJError,
    show: bool = True
) -> None:
    """
    Log a critical exception.

    Args:
        err (BaseException | BaseJError): Exception.
        show (bool): Show the error on terminal.
    """

def error(
    err: BaseException | JTKExternError.BaseJError,
    show: bool = True
) -> None:
    """
    Log an error exception.

    Args:
        err (BaseException | BaseJError): Exception.
        show (bool): Show the error on terminal.
    """

def warning(
    err: BaseException | JTKExternError.BaseJError,
    show: bool = True
) -> None:
    """
    Log a warning exception.

    Args:
        err (BaseException | BaseJError): Exception.
        show (bool): Show the error on terminal.
    """

@requires_init
def version(
    config: str,
    section: str,
    key: str
) -> JDEVersion:
    """
    Get a version from a config.

    Args:
        config (str): Config name.
        section (str): Config section name.
        key (str): Config setting name.

    Returns:
        JDEVersion: Version.
    """

@requires_init
def enabled(
    config: str,
    section: str,
    setting: str = "enabled"
) -> bool:
        """
        Get whether a setting is True or False.

        Args:
            config (str): Config name.
            section (str): Config section name.
            key (str): Config setting name.

        Returns:
            bool: Enabled or not.
        """

def get_registered_entities(
    category: str | None = None
) -> dict[str, JDEInternBaseClass]:
    """
    Get registered entities.

    Args:
        category (str | None): Entity category.

    Returns:
        dict[str, JDEInternBaseClass]: Registered entities.
    """

def get_registered_entity(
    name: str,
    *,
    category: str = "entity"
) -> JDEInternBaseClass:
    """
    Get a registered entity.

    Args:
        name (str): Entity name.
        category (str): Entity category.

    Returns:
        JDEInternBaseClass: Registered entity.
    """

__all__: Sequence[str] = [
    "assert_is_instance",
    "critical",
    "deprecated",
    "enabled",
    "error",
    "get_registered_entities",
    "get_registered_entity",
    "version",
    "warning",
]
