from collections import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, List, Mapping, Optional, Tuple, Type, get_type_hints

import decopatch
from fileflow.config import Config
from fileflow.file import File, Saveable


@dataclass
class Task:
    f: Callable
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]
    output_filetype: Type[File]


@dataclass
class Workflow:

    config: Config

    def __init__(self):
        self.tasks: List[Task] = []

    @decopatch.function_decorator
    def task(self, output: Optional[Type[File]] = None):
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
            elif output:
                output_filetype = output
            else:
                raise UserWarning(
                    f"""Cannot determine how to save output of {function}.
                    Either specify the "output" option of the "task" decorator,
                    or annotate the function with a return type that is a
                    subclass of "fileflow.Saveable"."""
                )

            @wraps(function)
            def new_function(*args, **kwargs):
                self.tasks.append(Task(function, args, kwargs, output_filetype))

            return new_function

        return decorate
