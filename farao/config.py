from dataclasses import dataclass
from os import getcwd
from pathlib import Path
from sys import path

from typeguard import check_type


@dataclass
class Config:
    output_root: Path

    def __post_init__(self):
        self.normalize()
        self.validate()

    def normalize(self):
        """To be extended by subclasses."""
        self.output_root = resolve_path(self.output_root)

    def validate(self):
        for name in dir(self):
            value = getattr(self, name)
            expected_type = self.__annotations__.get(name)
            if expected_type:
                try:
                    check_type(name, value, expected_type)
                except TypeError as e:
                    raise ConfigError(
                        f'The config setting "{name}" has an incorrect type. '
                        f'Expected type: "{expected_type}". '
                        f'Got type: "{type(value)}".'
                        f"See preceding exception for details."
                    ) from e


def resolve_path(path: str) -> Path:
    return Path(path).expanduser().resolve()


class ConfigError(Exception):
    """Raised when the user config cannot be loaded properly."""


def load_config(directory=None) -> Config:
    """
    Search the given directory (default: current working directory) for a
    file named "config.py" and import an object named "config" from it.
    """
    if directory is None:
        directory = getcwd()
    path.insert(0, str(directory))

    try:
        # Instruction for PyCharm code editor:
        # noinspection PyUnresolvedReferences
        from config import config
    except ModuleNotFoundError as err:
        raise ConfigError(
            f'Did not find a "config.py" file in {directory}'
        ) from err
    except ImportError as err:
        raise ConfigError(
            'Your "config.py" file must define an object named "config"'
        ) from err
    except TypeError as err:
        raise ConfigError(
            'Your custom "config" object could not be loaded.'
            " One of the specified arguments may have a wrong name."
            " See preceding exception for details."
        ) from err

    if not isinstance(config, Config):
        raise ConfigError(
            f'Your custom "config" object must be an instance of {Config} or'
            f" of a subclass of it, not {type(config)}."
        )

    return config
