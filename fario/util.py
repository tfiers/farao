from pathlib import Path
from typing import Union


def make_parent_dirs(file_path: Union[Path, str]):
    """
    Make sure the containing directories exist.

    :param file_path:  Pointing to a file in a directory.
    """
    dir_path: Path = Path(file_path).parent
    dir_path.mkdir(exist_ok=True, parents=True)
