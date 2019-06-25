from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    output_root: Path

    def __post_init__(self):
        self._normalize()
        self._validate()

    def _normalize(self):
        self.output_root = Path(self.output_root)

    def _validate(self):
        ...
