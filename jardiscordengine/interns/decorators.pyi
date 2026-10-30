from collections.abc import Callable, Sequence
from typing import Any, overload

def documented[T](
    cls: type[T]
) -> type[T]:
    """
    Add an automatic documentation to the class.
    Use on class.
    """

@overload
def register_entity[T](
    entity: T,
    *,
    name: str | None = None,
    category: str = "entity",
    replace: bool = False,
) -> T:
    """
    Register the entity to the global entity registry.
    Use on class.

    Args:
        name (str | None): Entity name.
        category (str): Registering category.
        replace (bool): Replace if already exists.
    """

@overload
def register_entity[T](
    entity: None = None,
    *,
    name: str | None = None,
    category: str = "entity",
    replace: bool = False,
) -> Callable[[T], T]:
    """
    Register the entity to the global entity registry.
    Use on class.

    Args:
        name (str | None): Entity name.
        category (str): Registering category.
        replace (bool): Replace if already exists.
    """

@overload
def logged[**P, R](
    func: Callable[P, R],
) -> Callable[P, R]:
    """
    Log the function at start and finish.
    Use on function.
    """

@overload
def logged[**P, R](
    func: None = None,
    *,
    title: str = "Call",
    level: str = "DEBUG",
    log_args: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Log the function at start and finish.
    Use on function.

    Args:
        title (str): Log title.
        level (str): Log level.
        log_args (bool): Log passed arguments.
    """

@overload
def handle_errors[**P, R](
    func: Callable[P, R],
) -> Callable[P, R]:
    """
    Handle errors.
    Use on function.
    """

@overload
def handle_errors[**P, R](
    func: None = None,
    *,
    reraise: bool = True,
    default: Any = None,
    keyboard_interrupt: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Handle errors.
    Use on function.

    Args:
        reraise (bool): Reraise after logging error.
        default (Any): Returned value when function fails.
        keyboard_interrupt (bool): Handle keyboard interruption (Ctrl+C)(reserved).
    """

@overload
def deprecated[**P, R](
    func: Callable[P, R],
) -> Callable[P, R]:
    """
    Warn when a function is deprecated.
    Use on function.
    """

@overload
def deprecated[**P, R](
    func: None = None,
    *,
    new_func: Callable[..., Any] | None = None,
    version: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Warn when a function is deprecated.
    Use on function.

    Args:
        new_func (Callable[..., Any] | None): New function that replaces the current one.
        version (str | None): Version from which the function is deprecated.
    """

@overload
def timed[**P, R](
    func: Callable[P, R],
) -> Callable[P, R]:
    """
    Log run time of the function.
    Use on function.
    """

@overload
def timed[**P, R](
    func: None = None,
    *,
    level: str = "DEBUG",
    title: str = "Timing",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Log run time of the function.
    Use on function.

    Args:
        level (str): Log level.
        title (str): Log title.
    """

def requires_init[**P, R](
    func: Callable[P, R]
) -> Callable[P, R]:
    """
    Don't run the function when JarDiscordEngine is not initialized.
    Use on function.
    """

class field[T]:
    """
    Create a typed field.
    Use in class.
    """

    expected_type: type[Any] | tuple[type[Any], ...] | None
    default: Any
    required: bool
    read_only: bool
    validator: Callable[[Any], bool] | None
    doc: str
    storage: str | None
    setter_check: Callable[[Any], bool] | None
    name: str
    owner: type[Any] | None

    @overload
    def __init__(
        self,
        expected_type: type[T] | tuple[type[Any], ...] | None = None,
        *,
        default: Any = ...,
        required: bool = False,
        read_only: bool = False,
        validator: Callable[[Any], bool] | None = None,
        doc: str = "",
        storage: str | None = None,
        setter_check: Callable[[Any], bool] | None = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        expected_type: type[Any] | tuple[type[Any], ...] | None,
        type_hint: type[T],
        *,
        default: Any = ...,
        required: bool = False,
        read_only: bool = False,
        validator: Callable[[Any], bool] | None = None,
        doc: str = "",
        storage: str | None = None,
        setter_check: Callable[[Any], bool] | None = None,
    ) -> None:
        ...

    def __set_name__(
        self,
        owner: type[Any],
        name: str) -> None:
            ...

    @overload
    def __get__(
        self,
        instance: None,
        owner: type[Any] | None = None
    ) -> field[T]:
        ...

    @overload
    def __get__(
        self,
        instance: Any,
        owner: type[Any] | None = None
    ) -> T:
        ...

    def __set__(
        self,
        instance: Any,
        value: T
    ) -> None:
        ...

    def __delete__(
        self,
        instance: Any
    ) -> None:
        ...

class flag[T]:
    """
    Create a typed attribute flag.
    Use in class.
    """

    obj: str
    name: str | None
    cast: Callable[[Any], T] | None
    doc: str
    owner: type[Any] | None
    public_name: str

    def __init__(
        self,
        obj: str = ".",
        *,
        name: str | None = None,
        cast: Callable[[Any], T] | None = None,
        doc: str = "",
    ) -> None: ...

    def __call__(
        self,
        func: Callable[[Any], str],
    ) -> flag[T]: ...

    def __set_name__(
        self,
        owner: type[Any],
        name: str
    ) -> None:
        ...

    @overload
    def __get__(
        self,
        instance: None,
        owner: type[Any] | None = None
    ) -> flag[T]:
        ...

    @overload
    def __get__(
        self,
        instance: Any,
        owner: type[Any] | None = None
    ) -> T:
        ...

    def __set__(
        self,
        instance: Any,
        value: T
    ) -> None:
        ...

    def __delete__(
        self,
        instance: Any
    ) -> None:
        ...

__all__: Sequence[str] = [
    "deprecated",
    "documented",
    "field",
    "flag",
    "handle_errors",
    "logged",
    "register_entity",
    "requires_init",
    "timed",
]
