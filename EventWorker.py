import time
import random
import logging
from pathlib import Path
from conf import settings
from celery.signals import after_setup_logger
from logging.handlers import TimedRotatingFileHandler
from Events.extended import ExtendedCelery, TaskFormatter

log = logging.getLogger()


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = TaskFormatter(
        '%(asctime)s - [%(root_id)s] - [%(task_id)s] - %(task_name)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    file_dir = f"{settings.BASE_DIR}{Path('/logs/celery.log')}"
    rf = TimedRotatingFileHandler(filename=file_dir, when='MIDNIGHT', interval=1, backupCount=0, encoding='utf-8')
    rf.setFormatter(formatter)
    logger.handlers = []
    logger.setLevel(logging.DEBUG)
    logger.addHandler(rf)
    logger.addHandler(sh)


app = ExtendedCelery('tasks')
app.config_from_object('conf.celery')


@app.task(bind=True, max_retries=5, acks_late=True)
def add(self, x, y):
    try:
        logging.info("add()")
        logging.debug("===---===")
        time.sleep(10)
        logging.debug("===---===")
        print(random.randint(1, 9699))
        return x + y
        # random_v = random.randint(1, 20)
        # print(f'random_v = {random_v}')
        # if random_v > 17:
        #     return x + y
        # else:
        #     raise Exception("random_v < 8")
    except Exception as e:
        print(e)
        self.retry(exec=e, countdown=1)




#  celery -A EventWorker worker -P solo -l debug -f logs/celery.log
#  celery -A EventWorker worker -P solo -l info
