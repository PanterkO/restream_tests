class TestData:

    def __init__(self):
        self.url = 'https://restream.sloppy.zone'
        self.login = 'restream5@mailinator.com'
        self.password = '123456'
        self.search_path = 'OWASP'
        self.search_result = None


class Product:

    def __init__(self, name='', description='', price=0):
        self.name = name
        self.description = description
        self.price = price


class Basket:

    def __init__(self):
        self.product_list = []

    def add(self, product):
        self.product_list.append(product)