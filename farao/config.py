from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from glob import glob
from importlib import import_module
from os import getcwd
from os.path import getmtime
from pathlib import Path
from pprint import pprint
from sys import path

import git
from typeguard import check_type


@dataclass
class Config:
    output_root: Path

    class RunInfoLogLevel(Enum):
        OFF = 0
        SHORT = 1
        FULL = 2

    run_info_log_level: RunInfoLogLevel = RunInfoLogLevel.SHORT

    def __post_init__(self):
        if self.run_info_log_level is not self.RunInfoLogLevel.OFF:
            self.log_run_info()
        self.normalize()
        self.validate()

    def log_run_info(self):
        cfg_class = self.__class__
        print(f"Loaded {cfg_class.__name__}:")
        pprint(asdict(self))
        top_level_package_name = cfg_class.__module__.split(".")[0]
        top_level_package = import_module(top_level_package_name)
        top_level_directory = top_level_package.__path__._path[0]
        source_files = glob(f"{top_level_directory}/**/*.py", recursive=True)
        mtimes = [getmtime(file) for file in source_files]
        last_modified = max(mtimes)
        last_modified_file = source_files[mtimes.index(last_modified)]
        if self.run_info_log_level is self.RunInfoLogLevel.FULL:
            print(
                f"{cfg_class} is part of package"
                f' "{top_level_package_name}", located at {top_level_directory}.'
                f" Last modified source file in this directory tree is:"
            )
        else:
            print("Last modified source file: ", end="")
        datetime_fmt = "%Y-%m-%d %H:%M:%S"
        print(
            f"{Path(last_modified_file).relative_to(top_level_directory)},"
            f" at {datetime.fromtimestamp(last_modified):{datetime_fmt}}",
            end=" ",
        )
        try:
            repo = git.Repo(top_level_directory, search_parent_directories=True)
            sha = repo.head.object.hexsha[:7]
            commit = repo.head.commit
            if self.run_info_log_level is self.RunInfoLogLevel.FULL:
                print(
                    f'\nPackage "{top_level_package_name}" is part of git repo at'
                    f" {repo.working_dir}, with latest commit at"
                    f" {commit.committed_datetime:{datetime_fmt}}"
                    f' ("{commit.message.strip()}", {sha})'
                )
            else:
                print(f"({sha})")
        except Exception as err:
            print(
                f"(Could not find git repo that {top_level_directory} is "
                f"part of. Reason: {err})"
            )

    def normalize(self):
        """To be extended by subclasses."""
        self.output_root = self.resolve_path(self.output_root)

    def validate(self):
        for name in dir(self):
            value = getattr(self, name)
            expected_type = self.__annotations__.get(name)
            if expected_type:
                try:
                    check_type(name, value, expected_type)
                except TypeError as e:
                    raise self.ConfigError(
                        f'The config setting "{name}" has an incorrect type. '
                        f'Expected type: "{expected_type}". '
                        f'Got type: "{type(value)}".'
                        f"See preceding exception for details."
                    ) from e

    @classmethod
    def load_from_directory(cls, directory=None) -> "Config":
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
            raise cls.ConfigError(
                f'Did not find a "config.py" file in {directory}'
            ) from err
        except ImportError as err:
            raise cls.ConfigError(
                'Your "config.py" file must define an object named "config"'
            ) from err
        except TypeError as err:
            raise cls.ConfigError(
                'Your custom "config" object could not be loaded.'
                " One of the specified arguments may have a wrong name."
                " See preceding exception for details."
            ) from err

        if not isinstance(config, Config):
            raise cls.ConfigError(
                f'Your custom "config" object must be an instance of {Config} or'
                f" of a subclass of it, not {type(config)}."
            )

        config: cls
        return config

    @staticmethod
    def resolve_path(path: str) -> Path:
        return Path(path).expanduser().resolve()

    class ConfigError(Exception):
        """Raised when the user config cannot be loaded properly."""
