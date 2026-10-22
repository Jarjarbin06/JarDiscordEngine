from typing import Literal, final

from jardiscordengine.interns.base_classe import JDEInternBaseClass
from jardiscordengine.interns.decorators import documentation
from jardiscordengine.interns.enums import JDEInternInstancePolicy

@documentation
@final
class JDEColor(
    JDEInternBaseClass[
        Literal[JDEInternInstancePolicy.NORMAL],
        Literal[0],
        Literal[False],
    ]
):
    """
    Version data.

    Attributes:
        r (int): Red channel.
        g (int): Green channel.
        b (int): Blue channel.
        a (int): Alpha channel.
        rgb (int): RGB channels.
        rgba (int): RGBA channels.
    """

    r: int
    g: int
    b: int
    a: int
    rgb: int
    rgba: int

    def __init__(
        self,
        r: int = 0,
        g: int = 0,
        b: int = 0,
        a: int = 255,
    ) -> None:
        """
        Initialize a color

        Args:
            r (int): Red channel (0 - 255)
            g (int): Green channel (0 - 255)
            b (int): Blue channel (0 - 255)
            a (int): Alpha channel (0 - 255)
        """
