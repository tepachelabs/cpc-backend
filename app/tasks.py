import logging
from datetime import datetime

from huey import MemoryHuey, FileHuey, crontab

from app.settings import PRODUCTION

logger = logging.getLogger(__name__)

huey = FileHuey() if PRODUCTION else MemoryHuey()


@huey.periodic_task(crontab(minute='*'))
def task_test():
    print(f"test: {datetime.now()}")
