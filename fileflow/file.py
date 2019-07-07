from abc import ABC, abstractstaticmethod
from pathlib import Path
from typing import Generic, Type, TypeVar


ContainedDatatype = TypeVar("ContainedDatatype")


class File(ABC, Generic[ContainedDatatype]):

    extension = ""
    # File extension, including leading dot. Subclasses should override at
    # class level.

    path: Path = ...

    def write(self, object: ContainedDatatype):
        """ Write a value to the file. """
        raise NotImplementedError

    def read(self) -> ContainedDatatype:
        """ Return the contents of the file. """
        raise NotImplementedError


class Saveable(ABC):
    """
    Mixin to mark an in-memory datatype as having a corresponding File
    subclass that can read/write instances of the datatype to disk.
    """

    @abstractstaticmethod
    @property
    def saveable_as() -> Type[File]:
        ...
