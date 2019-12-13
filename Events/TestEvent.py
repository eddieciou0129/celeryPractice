import logging
import time
import random
from .models.Product import Product
from EventWorker import app

log = logging.getLogger()


@app.task(bind=True, max_retries=5, acks_late=True)
def test_add(self, x, y):
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


@app.task(bind=True, max_retries=5, acks_late=True)
def send_order(self, product_pk, quantity, price):
    product = Product(product_pk)
    try:
        product.order(quantity, price)
        return '222'
    except Exception as exc:
        raise self.retry(exc=exc)



