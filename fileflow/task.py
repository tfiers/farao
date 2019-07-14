from dataclasses import dataclass
from typing import Any, Callable, Mapping, Tuple, Type

from fileflow.file import T, File


@dataclass
class Task:
    function: Callable
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def run(self):
        print(self)

    def __repr__(self):
        self.function
        return f"Task[{self.function.__qualname__}]"


@dataclass
class Future:
    filetype: Type[File[T]]
    task: Task
    index: Tuple[int, ...]

    def __repr__(self):
        return f"Future({self.filetype})"
