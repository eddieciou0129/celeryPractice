import time
import random
import logging
from celery import Celery
from conf import celery

app = Celery('tasks', broker=celery.BROKER_URL)


@app.task
def add(x, y):
    logging.info("add()")
    logging.debug("===---===")
    time.sleep(10)
    logging.debug("===---===")
    print(random.randint(1, 9699))
    return x + y

#  celery -A EventWorker worker -P solo --loglevel=info
