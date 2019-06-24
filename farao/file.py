import os
from abc import ABC
from pathlib import PosixPath, WindowsPath
from typing import TypeVar

from farao.util import make_parent_dirs


...
# We are not allowed to directly subclass "pathlib.Path". We therefore detect
# the OS and set the Path flavour manually).
if os.name == "nt":
    PathlibPath = WindowsPath
else:
    PathlibPath = PosixPath

T = TypeVar("T")


class File(PathlibPath, ABC):
    """
    Describes a file that is input/output to a task.
    """

    extension: str = ""
    # File extension, including leading dot. Subclasses should override at
    # class level.

    def write(self, object: T):
        """
        Write a value to the file.
        (Initial input files don't implement this).
        """

    def read(self) -> T:
        """
        Return the contents of the file.
        (Final output files don't implementthis).
        """

    def __new__(cls, path):
        make_parent_dirs(path)
        return PathlibPath.__new__(cls, path)

    @property
    def path_string(self):
        """ Path where this object is stored on disk, as a string. """
        return str(self)

    @property
    def size(self) -> str:
        """
        Giga and Mega are SI powers of 10 here -- not powers of 2 as Windows
        (wrongly) uses them (these are Gibi and Mebi).
        """
        size = self.stat().st_size  # In bytes
        for unit in ("bytes", "kB", "MB", "GB"):
            if size > 1000:
                size /= 1000
                continue
            else:
                break
        return f"{size:.1f} {unit}"
