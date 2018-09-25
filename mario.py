from abc import ABC, abstractmethod
from pathlib import Path


def File(Path):
    ...


class Task(ABC):
    @abstractmethod
    def run(self):
        ...
