from dataclasses import dataclass
from typing import Type, Sequence, Mapping, Any

from farao.file import File
from farao.config import Config


@dataclass
class ArgSpec:
    name: str
    type: Type
    # Type spec here is only for documentation purposes (We can't use it
    # programatically, as PyCharm does not resolve type annotations properly).


class FunctionSpec:
    input = ArgSpec("input", Sequence[File])
    output = ArgSpec("output", File)
    params = ArgSpec("params", Mapping[str, Any])
    config = ArgSpec("config", Config)
