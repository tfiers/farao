from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence, Type, get_type_hints

from farao.config import Config
from farao.file import File
from farao.spec import FunctionSpec


@dataclass
class Task:
    f: Callable
    input: Sequence[File]
    params: Mapping[str, Any]
    config: Config = None

    @property
    def output(self) -> File:
        return self._OutputType(self._output_path)

    @property
    def _OutputType(self) -> Type[File]:
        try:
            return get_type_hints(self.f)["output"]
        except KeyError as e:
            raise UserWarning(
                f'{self.f} should have an "output" argument'
            ) from e

    @property
    def _output_path(self) -> Path:
        # todo: naming algo: strip off common, handle multi input
        input_name_stems = []
        for file in self.input:
            input_name_stem = file.name.split(".", 1)[0]
            if input_name_stem not in input_name_stems:
                input_name_stems.append(input_name_stem)
            # rel_path = file.relative_to(self.config.output_root)
            # First directory of relative path is input task name. Subsequent
            # directories are params.
            # rel_path.parts
        filename = "__".join(input_name_stems)
        directory = self.config.output_root / self.f.__name__
        return directory / (filename + self._OutputType.extension)

    @property
    def f_kwargs(self):
        arguments = {
            FunctionSpec.input.name: self.input,
            FunctionSpec.output.name: self.output,
            FunctionSpec.params.name: self.params,
            FunctionSpec.config.name: self.config,
        }
        return {
            kwarg_name: value
            for kwarg_name, value in arguments.items()
            if kwarg_name in get_type_hints(self.f)
        }
