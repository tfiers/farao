from abc import ABC, abstractstaticmethod
from collections import Callable
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    get_type_hints,
)

import decopatch

from fileflow.config import Config
from fileflow.util import linearize


T = TypeVar("T")
# The datatype contained in the file, and represent by a Future.


class File(ABC, Generic[T]):

    extension = ""
    # File extension, including leading dot. Subclasses should override at
    # class level.

    path: Path = ...

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

    @abstractstaticmethod
    @property
    def saveable_as() -> Type[File]:
        ...


@dataclass
class Future(Generic[T]):
    """
    Represents (one of the) outputs of a task, that will be calculated later.
    """


@dataclass
class Task:
    f: Callable
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]
    saved: bool
    output_filetype: Type[File]


@dataclass
class Workflow:

    config: Config

    def __init__(self):
        self._tasks: List[Task] = []

    @decopatch.function_decorator
    def task(self, saved: bool = True):
        """
        The returned decorator makes any normal Python function into a task. It
        can be used both as "@my_workflow.task" and
        "@my_workflow.task(options)"
        """
        # decopatch makes it possible to use both invocations (normally "@task"
        # is an error and "@task()" should be used instead).

        def decorate(function: Callable):
            return_type = get_type_hints(function).get("return")
            if return_type and issubclass(return_type, Saveable):
                output_filetype = return_type
            else:
                msg = linearize(
                    f"""Cannot determine how to save output of {function}.
                    Annotate the function with a return type that is a subclass
                    of "fileflow.Saveable"."""
                )
                raise UserWarning(msg)

            @wraps(function)
            def new_function(*args, **kwargs) -> Task:
                new_task = Task(function, args, kwargs, saved, output_filetype)
                self._tasks.append(new_task)
                return new_task

            return new_function

        return decorate

    def register_filetype(self, datatype: Sequence[T], filetype: Type[File]):
        ...
