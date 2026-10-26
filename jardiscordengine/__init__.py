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
# License: GPL v3
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

from datetime import datetime as _datetime
from uuid import uuid4 as _uuid4

##Metadata##
__author__ = 'Nathan Jarjarbin'
__email__ = 'nathan.amaraggi@epitech.eu'
__version__ = "0.1.0"
__config_version__ = "0.1.0"
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

##Lifetime##
_start_time = None
_session = None

def init(project_path):
    global _start_time, _session

    Text = Interns.JTKExternConsole.Text

    _start_time = _datetime.now()
    _session = _uuid4().hex

    project_path = project_path.removesuffix("/")

    Interns.Config.JDEInternConfig.project_path = f"{project_path}"
    Interns.Config.JDEInternConfig.config_path = f"{project_path}/.jde-config"
    Interns.Config.JDEInternConfig.state_path = f"{project_path}/.jde-state"

    Interns.Log.JDEInternLog.project_path = f"{project_path}"
    Interns.Log.JDEInternLog.log_path = f"{project_path}/.jde-log"

    Interns.Config.init_all()

    Interns.Log.JDEInternLog("jde-log", _session=_session)

    name = Interns.Config.get('project', 'PROJECT', 'name', str, "Unnamed project")
    description = Interns.Config.get('project', 'PROJECT', 'description', str, "No description")
    version = Interns.Config.get('project', 'PROJECT', 'version', str, "0.0.0")
    author = Interns.Config.get('project', 'AUTHOR', 'name', str, None)
    organization = Interns.Config.get('project', 'AUTHOR', 'organization', str, None)

    sep = Text("───").f_layout_pad_center(80)

    top = Text(
        f"{_title_color(name)} {_version_color(version)}"
    ).f_layout_align_center(80)

    center = Text(
        f"{description}"
    ).f_layout_align_center(80)

    bottom = Text(
        f"Made by: {author}" + (f" ({organization})" if organization else "")
    ).f_layout_align_center(80)

    Interns.JTKExternConsole.Console.Console.print(
        Text(f"{top}\n{sep}\n{center}\n{sep}\n{bottom}").f_border_box(border=Interns.JTKExternConsole.PresetBorder.ROUND, padding=0),
        end="\n\n"
    )

    if not Interns.Config.get("state", "LAST_RUN", "clean_exit", bool, True):
        Interns.Helpers.warning(Interns.JTKExternError.JErrorRuntime("Previous run crashed"))

    Interns.Config.set("state", "LAST_RUN", "start", _start_time)
    Interns.Config.set("state", "LAST_RUN", "clean_exit", False)
    Interns.Config.set("state", "SESSION", "launches",  Interns.Config.get("state", "SESSION", "launches", int, 0) + 1)
    Interns.Config.set("state", "SESSION", "id", _session)
    Interns.Config.check_compatibility()

    Interns.Log.log("INFO", "ENGINE", f"JarDiscordEngine version {JDEVersion_JarDiscordEngine} initialized")
    Interns.Log.log("INFO", "ENGINE", f"Current session: {_session}")

    Interns.Log.save()

@Interns.Decorators.requires_init
def quit():
    global _session, _start_time

    if _start_time is not None and _session is not None:
        _end = _datetime.now()
        duration = (_end - _start_time).total_seconds()

        Interns.Config.set("state", "LAST_RUN", "end", _end)
        Interns.Config.set("state", "LAST_RUN", "duration", duration)

        total_runtime = Interns.Config.get("state", "STATISTICS", "total_runtime", float, 0.0)
        launches = Interns.Config.get("state", "SESSION", "launches", int, 1)
        longest_session = Interns.Config.get("state", "STATISTICS", "longest_session", float, 0.0)
        shortest_session = Interns.Config.get("state", "STATISTICS", "shortest_session", float, 0.0)

        new_total_runtime = total_runtime + duration  # pyright: ignore[reportOperatorIssue]
        average_session = new_total_runtime / launches

        longest_session = max(longest_session, duration)

        if shortest_session == 0 or duration < shortest_session:  # pyright: ignore[reportOperatorIssue]
            shortest_session = duration

        Interns.Config.set("state", "STATISTICS", "total_runtime", new_total_runtime)
        Interns.Config.set("state", "STATISTICS", "average_session", average_session)
        Interns.Config.set("state", "STATISTICS", "longest_session", longest_session)
        Interns.Config.set("state", "STATISTICS", "shortest_session", shortest_session)

    Interns.Log.log("INFO", "ENGINE", "Engine quit")
    Interns.Log.save()
    Interns.Log.close()

    Interns.Config.set("state", "LAST_RUN", "clean_exit", True)

    _start_time = None
    _session = None

##Special##
def _title_color(title):

    return Interns.JTKExternConsole.Text(title).f_color_foreground(Interns.JTKExternConsole.ColorRGB(70, 160, 255))

def _subtitle_color(title):

    return Interns.JTKExternConsole.Text(title).f_color_foreground(Interns.JTKExternConsole.ColorRGB(47, 107, 170))

def _version_color(version):

    return Interns.JTKExternConsole.Text(version).f_color_foreground(Interns.JTKExternConsole.ColorRGB(150, 150, 150))

def _banner():
    Text = Interns.JTKExternConsole.Text
    Cursor = Interns.JTKExternConsole.ANSI.Cursor.CursorPosition
    Screen = Interns.JTKExternConsole.ANSI.Screen.ScreenErase

    sep = Text("───").f_layout_pad_center(80)

    top = Text(
        f"{_title_color("JarDiscordEngine (JDE)")} {_version_color(__version__)}"
    ).f_layout_align_center(80)

    center = Text(
        f"{_subtitle_color("Config")} {_version_color(JDEVersion_Config)} ─ "
        f"{_subtitle_color("Py-Cord")} {_version_color(JDEVersion_Discord)} ─ "
        f"{_subtitle_color("Python")} {_version_color(JDEVersion_Python)}"
    ).f_layout_align_center(80)

    bottom = Text(
        "Discord bot development framework"
    ).f_layout_align_center(80)

    Interns.JTKExternConsole.Console.Console.print(
        (f"{Cursor.previous_line() + Screen.erase_line()}" * 2) +
        Text(f"{top}\n{sep}\n{center}\n{sep}\n{bottom}").f_border_box(border=Interns.JTKExternConsole.PresetBorder.ROUND, padding=0),
        end="\n\n"
    )

def _validate_all_instance_policies() -> None:
    for subclass in Interns.JDEInternBaseClass.__subclasses__():
        subclass.validate_instance_policies()  # pyright: ignore[reportAttributeAccessIssue]


__all__ = [  # noqa: RUF022
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
    'JDEVersion_JarDiscordEngine',
    'JDEVersion_Python',
    # Booleans #
    'JDEFalse',
    'JDETrue',
]

_banner()
_validate_all_instance_policies()
