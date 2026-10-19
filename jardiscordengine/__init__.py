# =============================================================================
# JarDiscordEngine - Python Discord Bot Engine (pycord-based)
# =============================================================================
#
# JarDiscordEngine is a lightweight bot framework built on top of pycord
# that simplifies Discord bot development while providing higher-level
# abstractions for command management, event handling, and extensibility.
#
# =============================================================================
# Version: jardiscordengine-v1
# Author: Jarjarbin Studio
# Licence: GPL v3
# =============================================================================
#
# This engine is inspired by pycord, modern bot framework design patterns,
# and modular software architecture.
#
# It is designed for educational purposes and small-to-medium Discord bot
# projects.
#
# It provides structured systems such as automatic command discovery,
# command registration, event handling, extension management, and shared
# services for logging, configuration, and permissions.
#
# =============================================================================
# WARNING:
# =============================================================================
#
# This is NOT pycord itself.
# It is a custom abstraction layer built on top of pycord.
#
# =============================================================================

from __future__ import annotations

##Metadata##
__author__ = 'Nathan Jarjarbin'
__email__ = 'nathan.amaraggi@epitech.eu'
__version__ = "0.1.0"
__license__ = "GPL"

##Imports##
import jardiscordengine.bots as Bots
import jardiscordengine.commands as Commands
import jardiscordengine.entities as Entities
import jardiscordengine.events as Events
import jardiscordengine.extensions as Extensions
import jardiscordengine.interns as Interns
import jardiscordengine.services as Services
import jardiscordengine.systems as Systems

from jardiscordengine.constants import *

##Special##
def _title_color(title):

    return Interns.JTKExternConsole.Text(title).f_color_foreground(Interns.JTKExternConsole.ColorRGB(70, 160, 255))

def _version_color(version):

    return Interns.JTKExternConsole.Text(version).f_color_foreground(Interns.JTKExternConsole.ColorRGB(150, 150, 150))

def _banner():
    Text = Interns.JTKExternConsole.Text
    Cursor = Interns.JTKExternConsole.ANSI.Cursor.CursorPosition
    Screen = Interns.JTKExternConsole.ANSI.Screen.ScreenErase

    top = Text(
        f"{_title_color("JarDiscordEngine (JDE)")} {_version_color(__version__)}"
    ).f_layout_align_center(50)

    center = Text("-").f_layout_pad_center(50)

    bottom = Text(
        f"Discord bot development framework"
    ).f_layout_align_center(50)

    Interns.JTKExternConsole.Console.Console.print(
        (f"{Cursor.previous_line() + Screen.erase_line()}" * 2) +
        Text(f"{top}\n{center}\n{bottom}").f_border_box(border=Interns.JTKExternConsole.PresetBorder.ROUND, padding=0),
        end="\n\n"
    )

def _validate_all_instance_policies() -> None:
    for subclass in Interns.JDEInternBaseClass.__subclasses__():
        subclass.validate_instance_policies()

__all__ = [
    ## Special ##
    "__author__",
    "__email__",
    "__version__",
    "__license__",
    ## Imports ##
    'Bots',
    'Commands',
    'Entities',
    'Events',
    'Extensions',
    'Interns',
    'Services',
    'Systems',
    ## Constants ##
    # Versions #
    'JDEVersion_JarEngine',
    'JDEVersion_Python',
    # Booleans #
    'JDEFalse',
    'JDETrue',
]

_banner()
_validate_all_instance_policies()
