from farao.config import Config, load_config
from farao.file import File
from farao.schedule import Scheduler


# A default scheduler:
schedule = Scheduler(Config(output_root="."))
