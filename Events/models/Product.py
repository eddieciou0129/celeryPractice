

class Product(object):
    def __init__(self, product_pk):
        self._product_pk = product_pk

    def order(self, quantity, price):
        print(f'{self._product_pk}, quantity={quantity}, price={price}')
        raise Exception('258')

