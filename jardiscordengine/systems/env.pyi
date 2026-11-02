from collections.abc import Sequence
from typing import Any

class JDEEnvMeta(
    type
):

    @classmethod
    def __call__(
        cls,
        setting: str,
        default: Any = None
    ) -> str:
        """
        Get env variable.

        Args:
            setting (str): Variable name.
            default (Any): Default value.

        Returns:
            str: Value.
        """

class JDEEnv(
    metaclass=JDEEnvMeta
):

    @staticmethod
    def load(
        path: str | None= None
    ) -> None:
        """
        Load `.env` file environment.

        Args:
            path (str | None): File path.
        """

    @staticmethod
    def set(
        setting: str,
        value: Any
    ) -> None:
        """
        Set env variable.

        Args:
            setting (str): Variable name.
            value (Any): New value.
        """

    @staticmethod
    def contains(
        setting: str
    ):
        """
        Check if the env has a variable.

        Args:
            setting (str): Variable name.
        """

__all__: Sequence[str] = [
    "JDEEnv",
]
