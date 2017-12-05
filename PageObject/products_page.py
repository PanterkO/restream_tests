import time

from models.data import Basket, Product


def without_links(text):
    import re
    p = re.findall(r'<.*?>', text)
    for i in p:
        text = text.replace(i, '')

    return re.sub(r'\s+', ' ', text)


class ProductsPage:
    def __init__(self, driver):
        self.driver = driver

    def search_product(self, product):
        # with open(os.getcwd()+'/script.js') as script:
        #    self.wd.execute_script(script.read())
        self.driver.wd.find_element_by_xpath('//nav//input[@ng-model="searchQuery"]').send_keys(product)
        self.driver.wd.find_element_by_xpath('//*[@id="searchButton"]').click()
        self.driver.data.search_result = self.driver.wd.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')

    def assert_search_result(self):
        time.sleep(.5)
        # достаем все товары из результатов поиска
        search_results = self.driver.wd.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
        product_list = Basket()
        for result in search_results:
            product = Product()
            product.name = result.find_element_by_xpath('.//td[2]').text
            product.description = result.find_element_by_xpath('.//td/div[@ng-bind-html="product.description"]').text
            product.price = float(result.find_element_by_xpath('.//td[4]').text)
            product.image = result.find_element_by_xpath('.//td/img').get_attribute("src")
            product_list.add(product)
        # todo достаем ответ из api
        '''
        import requests
        params = {'q': self.driver.data.search_path}
        url = self.driver.data.url+'/rest/product/search?q=OWASP'
        responce = requests.get(url=url)
        print(responce.json())
        requests.exceptions.ProxyError: HTTPSConnectionPool(host='restream.sloppy.zone', port=443): Max retries exceeded with url: /rest/product/search?q=OWASP (Caused by ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 407 Proxy Authentication Required',)))

        '''
        # todo подумать, как достать тест с ссылками
        import json
        with open('responce.json') as r:
            responce = json.load(r)
        product_list_from_api = Basket()
        for r in responce['data']:
            product = Product()
            product.name = r['name']
            product.description = without_links(r['description'])
            product.price = float(r['price'])
            product.image = r['image']
            product_list_from_api.add(product)
        assert len(product_list.product_list) == len(product_list_from_api.product_list)
        for i in range(0, len(product_list.product_list) - 1):
            assert product_list.product_list[i].name == product_list_from_api.product_list[i].name, \
                'Название товара {} не соответствует API:{}'.format(product_list.product_list[i].name,
                                                                    product_list_from_api.product_list[i].name)
            assert product_list.product_list[i].description == product_list_from_api.product_list[i].description, \
                'Описание товара {} не соответствует API:{}'.format(product_list.product_list[i].description,
                                                                    product_list_from_api.product_list[i].description)
            assert product_list.product_list[i].price == product_list_from_api.product_list[i].price, \
                'Цена товара {} не соответствует API:{}'.format(product_list.product_list[i].price,
                                                                product_list_from_api.product_list[i].price)
            assert product_list_from_api.product_list[i].image in product_list.product_list[i].image, \
                'Изображение товара {} не соответствует API:{}'.format(product_list.product_list[i].image,
                                                                       product_list_from_api.product_list[i].image)

    def assert_every_product_have_icons_show_details_and_add_to_basket(self, products):

        for product in products:
            try:
                product.find_element_by_xpath('.//i[contains(@class, "fa-eye")]')
                show_details_is_present = True
            except:
                show_details_is_present = False

            try:
                product.find_element_by_xpath('.//i[contains(@class, "fa-cart-plus")]')
                add_to_basket_is_present = True
            except:
                add_to_basket_is_present = False

            assert show_details_is_present is True, 'Icon ShowDetails is not found for {}'.format(
                product.find_element_by_xpath('.//td[2]').text)
            assert add_to_basket_is_present is True, 'Icon AddToBasket is not found for {}'.format(
                product.find_element_by_xpath('.//td[2]').text)

    def add_the_cheapest_product_to_basket(self, search_result):

        cheapest_wear = self.search_the_cheapest_product(search_result)
        cheapest_wear.find_element_by_xpath('./td[5]//i[contains(@class, "fa-cart-plus")]').click()
        max_price = float(cheapest_wear.find_element_by_xpath('./td[4]').text)
        cheapest_wear = self.search_the_cheapest_product(search_result, max_price)
        cheapest_wear.find_element_by_xpath('./td[5]//i[contains(@class, "fa-cart-plus")]').click()

    def search_the_cheapest_product(self, products, max_previous_price=9223372036854775807):
        max_price = 0
        for product in products:
            price = float(product.find_element_by_xpath('./td[4]').text)
            if price > max_price and price < max_previous_price:
                max_price = price
                cheapest_wear = product
        return cheapest_wear
