from collections import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Dict, List, Sequence, Type, get_type_hints, Union, Tuple

from fileflow.config import Config
from fileflow.file import File, Saveable, T
from fileflow.task import Task, Future
from fileflow.util import linearize


@dataclass
class Workflow:

    config: Config

    def __post_init__(self):
        self._tasks: List[Task] = []
        mapping = Dict[Type[T], Type[File]]
        self._registered_filetypes: mapping = dict()

    def register_filetype(
        self, datatype: Union[Type[T], Sequence[Type[T]]], filetype: Type[File]
    ):
        try:
            datatype = list(datatype)
        except TypeError:
            datatype = [datatype]
        for t in datatype:
            self._registered_filetypes[t] = filetype

    def task(self, function: Callable):
        """
        Decorate any normal Python function into a task.
        """
        return_type = get_type_hints(function).get("return")

        @wraps(function)
        def new_function(*args, **kwargs) -> Task:
            new_task = Task(function, args, kwargs)
            future_tuple = self._futurize_type(return_type, new_task)
            self._tasks.append(new_task)
            return future_tuple

        return new_function

    def run(self):
        for task in self._tasks:
            task.run()
        print("All done :)")

    def _futurize_type(
        self,
        type: Type[Union[Tuple, T]],
        task: Task,
        index: Tuple[int, ...] = (),
    ) -> Union[Future, Tuple]:
        name = getattr(type, "_name", None)
        if name == "Tuple":
            contents = type.__args__
            return tuple(
                self._futurize_type(type, task, index + (i,))
                for i, type in enumerate(contents)
            )
        else:
            try:
                filetype = self._get_output_filetype(type)
                return Future(filetype, task, index)
            except Exception as err:
                error_message = linearize(
                    f"""Could not determine how to save output of {task}.
                    Either annotate the function with a return type that is a
                    subclass of "fileflow.Saveable", or call
                    "register_filetype" on your Workflow."""
                )
                raise UserWarning(error_message) from err

    def _get_output_filetype(self, datatype: Type[T]) -> Type[File]:
        if datatype in self._registered_filetypes:
            return self._registered_filetypes[datatype]
        elif issubclass(datatype, Saveable):
            return datatype.get_filetype()
        else:
            raise Exception
