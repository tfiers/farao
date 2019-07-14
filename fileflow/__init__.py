from pkg_resources import get_distribution

__version__ = get_distribution(__name__).version
print(f"This is FileFlow version {__version__}")

from fileflow.config import Config
from fileflow.workflow import Workflow
from fileflow.task import Task, Future
from fileflow.file import File, Saveable
