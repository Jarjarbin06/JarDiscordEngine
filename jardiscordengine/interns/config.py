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
from pathlib import Path as _Path
from typing import final as _final

from jardiscordengine.interns import JTKExternConfig as _JTKExternConfig
from jardiscordengine.interns import JTKExternError as _JTKExternError
from jardiscordengine.interns.base_classe import (
    JDEInternBaseClass as _JDEInternBaseClass,
)
from jardiscordengine.interns.decorators import documented as _documented
from jardiscordengine.interns.decorators import requires_init as _requires_init
from jardiscordengine.interns.enums import (
    JDEInternInstancePolicy as _JDEInternInstancePolicy,
)

CONFIGS = {}

@_documented
@_final
class JDEInternConfig(_JTKExternConfig.Config, _JDEInternBaseClass):

    __instance_policy__ = _JDEInternInstancePolicy.UNIQUE
    __instance_limit__ = 0
    __recursive__ = False

    project_path = None
    config_path = None
    state_path = None

    @_requires_init
    def __new__(cls, name, data, is_state, _jde_key=None, _jde_warn=None, **kwargs):
        return _JDEInternBaseClass.__new__(
            cls,
            _jde_key=_jde_key if _jde_key is not None else name,
            _jde_warn=_jde_warn,
        )

    @_requires_init
    def __init__(
        self,
        name,
        data = None,
        is_state = False,
        *,
        metadata = None,
        has_extension = True,
        _token = None,
    ):
        if not JDEInternConfig.project_path or not (
            JDEInternConfig.state_path if is_state
            else JDEInternConfig.config_path
        ):
            raise _JTKExternError.JErrorRuntime(
                "JarDiscordEngine.init(path) must be called first"
            )

        if _token is not None:
            _JTKExternConfig.Config.__init__(
                self,
                JDEInternConfig.config_path,  # pyright: ignore[reportArgumentType]
                name,
                metadata=metadata,
                has_extension=has_extension,
                _token=_token,
            )
            return

        from jardiscordengine.constants import (
            JDEVersion_Config as _JDEVersion_Config,
        )
        from jardiscordengine.constants import (
            JDEVersion_JarDiscordEngine as _JDEVersion_JarDiscordEngine,
        )

        config_directory = _Path(
            JDEInternConfig.state_path  # pyright: ignore[reportArgumentType]
            if is_state
            else JDEInternConfig.config_path
        )

        if data is None:
            data = {}

        if not isinstance(data, dict):
            raise _JTKExternError.JErrorType(
                "Config data must be a dictionary"
            )

        file_name = f"je-{name}"

        try:
            try:
                config = _JTKExternConfig.Config.open(
                    config_directory,
                    file_name,
                )
            except _JTKExternConfig.ConfigFileNotFoundJError:
                config = _JTKExternConfig.Config.create(
                    config_directory,
                    file_name,
                )

                config.set_batch({
                    "INFO": {
                        "name": name,
                        "creation": _datetime.now().isoformat(),
                        "jardiscordengine_version": str(_JDEVersion_JarDiscordEngine),
                        "config_version": str(_JDEVersion_Config),
                    },
                    **data,
                })
            else:
                for section, options in data.items():
                    if not config.section_exists(section):
                        config.section_add(section)

                    for option, value in options.items():
                        if not config.option_exists(section, option):
                            config.set(section, option, value)


        except _JTKExternConfig.ConfigValueJError as error:
            raise _JTKExternError.JErrorKey(
                str(error)
            ) from error
        except _JTKExternConfig.ConfigRuntimeJError as error:
            raise _JTKExternError.JErrorRuntime(
                str(error)
            ) from error

        self.__dict__.update(config.__dict__)

        self.config_name = name
        self.is_state = is_state

        _JDEInternBaseClass.__init__(self)

        CONFIGS[name] = self

@_requires_init
def get(name, section, setting, type = str, default = None):
    if name not in CONFIGS:
        raise _JTKExternError.JErrorFileNotFound(
            f"No config named {name} is opened"
        )

    config = CONFIGS[name]

    getters = {
        str: config.get,
        bool: config.get_bool,
        int: config.get_int,
        float: config.get_float,
    }

    try:
        getter = getters.get(type)

        if getter is not None:
            return getter(section, setting)

        # Support other types through explicit conversion.
        return type(config.get(section, setting))

    except _JTKExternConfig.ConfigTypeJError as error:
        if default is not None:
            return default
        raise _JTKExternError.JErrorType(
            "Invalid value type"
        ) from error

    except _JTKExternConfig.ConfigValueJError as error:
        if default is not None:
            return default
        raise _JTKExternError.JErrorKey(
            "Section or setting not found"
        ) from error

    except (ValueError, TypeError) as error:
        if default is not None:
            return default
        raise _JTKExternError.JErrorType(
            "Invalid value type"
        ) from error

@_requires_init
def set(name, section, setting, value):
    if name not in CONFIGS:
        raise _JTKExternError.JErrorFileNotFound(
            f"No config named {name} is opened"
        )

    try:
        CONFIGS[name].set(
            section,
            setting,
            value,
        )
    except _JTKExternConfig.ConfigValueJError as error:
        raise _JTKExternError.JErrorKey(
            str(error)
        ) from error

@_requires_init
def init_all():
    from jardiscordengine.constants import (
        JDEVersion_Config as _JDEVersion_Config,
    )
    from jardiscordengine.constants import (
        JDEVersion_Discord as _JDEVersion_Discord,
    )
    from jardiscordengine.constants import (
        JDEVersion_JarDiscordEngine as _JDEVersion_JarDiscordEngine,
    )
    from jardiscordengine.constants import (
        JDEVersion_Python as _JDEVersion_Python,
    )

    JDEInternConfig(
        "project",
        {
            "PROJECT": {
                "name": "Unnamed project",
                "description": "No description",
                "version": "0.1.0",
                "jardiscordengine_version": str(_JDEVersion_JarDiscordEngine),
                "config_version": str(_JDEVersion_Config),
                "pycord_version": str(_JDEVersion_Discord),
                "python_version": str(_JDEVersion_Python),
            },
            "AUTHOR": {
                "name": "Anonym",
                "organization": "",
            },
        },
        False,
    )

    JDEInternConfig(
        "state",
        {
            "FIRST_RUN": {
                "timestamp": _datetime.now().isoformat(),
            },
            "LAST_RUN": {
                "start": "",
                "end": "",
                "duration": "",
                "clean_exit": True,
            },
            "SESSION": {
                "launches": 0,
            },
            "STATISTICS": {
                "total_runtime": 0.0,
                "average_session": 0.0,
                "longest_session": 0.0,
                "shortest_session": 0.0,
            },
        },
        True,
    )

@_requires_init
def check_compatibility():
    from jardiscordengine.constants import JDEVersion_Config as _JDEVersion_Config
    from jardiscordengine.constants import JDEVersion_Discord as _JDEVersion_Discord
    from jardiscordengine.constants import (
        JDEVersion_JarDiscordEngine as _JDEVersion_JarDiscordEngine,
    )
    from jardiscordengine.constants import JDEVersion_Python as _JDEVersion_Python
    from jardiscordengine.interns.helpers import (
        error as _error,
    )
    from jardiscordengine.interns.helpers import (
        version as _version,
    )
    from jardiscordengine.interns.helpers import (
        warning as _warning,
    )
    from jardiscordengine.systems.enums import JDECompatibility as _JDECompatibility

    def _check(current, required, name):
        status = current.compatibility(required)

        if status != _JDECompatibility.OK:
            err = _JTKExternError.BaseJError(
                f"Compatibility failure on {name} "
                f"(current: {current}, required: {required})"
            )

            if status == _JDECompatibility.ERROR:
                _error(err)

            elif status == _JDECompatibility.WARNING:
                _warning(err)

    required_engine = _version("project", "PROJECT", "jardiscordengine_version")
    required_config = _version("project", "PROJECT", "config_version")
    required_pycord = _version("project", "PROJECT", "pycord_version")
    required_python = _version("project", "PROJECT", "python_version")

    _check(_JDEVersion_JarDiscordEngine, required_engine, "JarDiscordEngine version")
    _check(_JDEVersion_Config, required_config, "Config version")
    _check(_JDEVersion_Discord, required_pycord, "Discord version")
    _check(_JDEVersion_Python, required_python, "Python version")

    for config in CONFIGS:

        _check(
            _version(config, "INFO", "jardiscordengine_version"),
            required_engine,
            f"{get(config, 'INFO', 'name')} JarDiscordEngine version"
        )

        _check(
            _version(config, "INFO", "config_version"),
            required_config,
            f"{get(config, 'INFO', 'name')} Config version"
        )

__all__ = [
    "CONFIGS",
    "JDEInternConfig",
    "check_compatibility",
    "get",
    "init_all",
    "set"
]
