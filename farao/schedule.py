from typing import Any, Callable, Dict, List, Mapping, Optional

from farao.config import Config
from farao.file import File
from farao.task import OneOrMore, Task


class Scheduler:
    """
    A collection of Tasks. Call as a function to add a task.
    """

    tasks: List[Task]
    outputs: Dict[str, Task]

    def __init__(self, config: Config):
        self.tasks = []
        self.outputs = {}
        self.config = config

    def __call__(
        self,
        f: Callable,
        input: OneOrMore[File],
        output: OneOrMore[File],
        params: Mapping[str, Any] = None,
    ) -> File:
        new_task = Task(f, input, output, params, self.config)
        output_key = str(output)
        if output_key in self.outputs:
            conflicting_task = self.outputs[output_key]
            print(
                f"Error adding {repr(new_task)}: a task with the same output has"
                f" already been added: {repr(conflicting_task)}"
            )
        else:
            self.tasks.append(new_task)
            self.outputs[output_key] = new_task
            return output

    def run_sequentially(self):
        for task in self.tasks:
            task.run()
        print("All tasks completed succesfully :)")

    def get_airflow_DAG(self):
        ...
