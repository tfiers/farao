from farao.file import File
from farao.schedule import Scheduler
from farao.config import Config


# A light API:
default_scheduler = Scheduler(Config(output_root="."))


def set_config(cfg: Config):
    if not default_scheduler.tasks:
        default_scheduler.config = cfg
    else:
        raise UserWarning(
            "Global task config should be set before any tasks are scheduled."
        )


schedule = default_scheduler.schedule
run_all = default_scheduler.run_all
