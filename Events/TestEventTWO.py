import logging
from celery import Task
from .models.Product import Product
from EventWorker import app


class SendOrder(Task):
    max_retries = 5
    acks_late = True
    name = 'payment.check_withdrawal_status'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self, product_pk, quantity, price):
        product = Product(product_pk)
        try:
            product.order(quantity, price)
            return '222'
        except Exception as e:
            print("OOO")
            print(e)
            self.retry(exe=e, countdown=1)


app.register_task(SendOrder())
