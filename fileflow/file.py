from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Type, TypeVar


...
# The datatype output by a function, and contained in a File.
T = TypeVar("T")


@dataclass
class File(ABC, Generic[T]):

    path: Path

    extension = ""
    # File extension, including leading dot. Subclasses should override at
    # class level.

    def write(self, object: T):
        """ Write a value to the file. """
        raise NotImplementedError

    def read(self) -> T:
        """ Return the contents of the file. """
        raise NotImplementedError


class Saveable(ABC):
    """
    Mixin to mark an in-memory datatype T as having a corresponding File
    subclass that can read/write instances of the datatype to disk.
    """

    @staticmethod
    @abstractmethod
    def get_filetype() -> Type[File]:
        ...
