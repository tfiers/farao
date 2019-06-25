from typing import Any, Callable, Mapping, Sequence

from farao.config import Config
from farao.file import File
from farao.task import Task


class Scheduler:
    tasks = []

    def __init__(self, config: Config):
        self.config = config

    def schedule(
        self,
        f: Callable,
        input: Sequence[File],
        params: Mapping[str, Any] = None,
    ) -> File:
        new_task = Task(f, input, params, self.config)
        self.tasks.append(new_task)
        return new_task.output

    def run_all(self):
        for task in self.tasks:
            print(f"Running {task.f} with arguments {task.f_kwargs}")
            # task.f(**kwargs)
