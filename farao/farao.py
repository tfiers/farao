from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence, TypeVar, Union

from farao import File


T = TypeVar("T")
OneOrMore = Union[T, Sequence[T]]
ParamDict = Mapping[str, Any]


tasks = []


def run():
    ...


@dataclass
class Task:
    f: Callable[[OneOrMore[File], ParamDict], OneOrMore[File]]
    inputs: OneOrMore[File]
    params: ParamDict

    def __post_init__(self):
        tasks.append(self)


# Syntactic sugar:
scheduled = Task
