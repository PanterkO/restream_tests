class TestData:

    def __init__(self):
        self.url = 'https://restream.sloppy.zone'
        self.login = 'restream5@mailinator.com'
        self.password = '123456'
        self.search_path = 'OWASP'
        self.search_result = None
        self.pre_basket = None
        self.basket = None


class Product:

    def __init__(self, name='', description='', price=0, image=''):
        self.name = name
        self.description = description
        self.price = price
        self.image = image

    def parse(self, result):
        self.name = result.find_element_by_xpath('.//td[2]').text
        self.description = result.find_element_by_xpath('.//td/div[@ng-bind-html="product.description"]').text
        self.price = float(result.find_element_by_xpath('.//td[4]').text)
        self.image = result.find_element_by_xpath('.//td/img').get_attribute("src")


class Basket:

    def __init__(self):
        self.product_list = []

    def add(self, product):
        self.product_list.append(product)

