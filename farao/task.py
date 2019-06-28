from os import getcwd
from typing import Callable, Optional, Tuple, TypeVar, Union, get_type_hints

from farao.file import File


T = TypeVar("T")
OneOrMore = Union[T, Tuple[T, ...]]

from dataclasses import dataclass
from typing import Any, Mapping, Type

from farao.config import Config


@dataclass
class ArgSpec:
    name: str
    type: Type
    # Nota: we can't use this type in our own type hints, as PyCharm does not
    # resolve type annotations properly.
    optional: bool = False


f_argspec = (
    ArgSpec("input", OneOrMore[File]),
    ArgSpec("output", OneOrMore[File]),
    ArgSpec("params", Mapping[str, Any], optional=True),
    ArgSpec("config", Config, optional=True),
)


@dataclass
class Task:
    f: Callable
    input: OneOrMore[File]
    output: OneOrMore[File]
    params: Mapping[str, Any]
    config: Config
    output_name: Optional[str] = None

    def run(self):
        """ Atomically execute function, if it hasn't completed yet. """
        if self.output.exists():
            print(f"Skipping {self}, as its output already exists.")
        else:
            print(f"Running {self}")
            try:
                self.f(**self._f_kwargs)
                print(f"{self} completed succesfully")
            except Exception as err:
                print(f"{self} failed (exception follows).")
                if self.output.exists():
                    # Delete possibly incomplete or corrupt output.
                    self.output.delete()
                raise err

    def __repr__(self):
        """ A full representation. """
        kwargs = [f"{k}={v}" for k, v in self._f_kwargs.items()]
        return f"Task({self.f.__name__}, {', '.join(kwargs)})"

    def __str__(self):
        """ A short, friendly representation. """
        return f"Task({self.output.relative_to(getcwd())})"

    def __post_init__(self):
        self._validate()

    def _validate(self):
        args = get_type_hints(self.f)
        f_name = self.f.__name__
        for arg in f_argspec:
            if not arg.optional and arg.name not in args:
                raise UserWarning(
                    f'{f_name} should have an argument "{arg.name}" with type'
                    f" annotation {arg.type}."
                )
            if arg.name in args:
                ...
                # Checking if type annotation is correct seems difficult.
        # Check self.input etc directly here, with typeguard.check_type

    @property
    def _f_kwargs(self):
        arguments = dict(
            input=self.input,
            output=self.output,
            params=self.params,
            config=self.config,
        )
        return {
            kwarg_name: value
            for kwarg_name, value in arguments.items()
            if kwarg_name in get_type_hints(self.f)
        }
        # Fix: not based on type hints, but presence of arg. ie. inspect module.


def as_tuple(obj: OneOrMore[T]) -> Tuple[T, ...]:
    try:
        return tuple(obj)
    except TypeError:
        return (obj,)
