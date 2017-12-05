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

        driver = self.driver.wd
        driver.find_element_by_xpath('//nav//input[@ng-model="searchQuery"]').send_keys(product)
        driver.find_element_by_xpath('//*[@id="searchButton"]').click()
        self.driver.data.search_result = driver.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')

    def assert_search_result_is_correct(self):

        time.sleep(.5)
        # достаем все товары из результатов поиска
        driver = self.driver.wd
        search_results = driver.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
        products = Basket()
        for result in search_results:
            product = Product()
            product.parse(result)
            products.add(product)

        import requests
        params = {'q': self.driver.data.search_path}
        url = self.driver.data.url+'/rest/product/search'
        request = requests.get(url=url, params=params)
        responce = request.json()
        products_api = Basket()
        for r in responce['data']:
            product = Product()
            product.name = r['name']
            product.description = without_links(r['description'])
            product.price = float(r['price'])
            product.image = r['image']
            products_api.add(product)
        assert len(products.product_list) == len(products_api.product_list)
        for i in range(0, len(products.product_list) - 1):
            assert products.product_list[i].name == products_api.product_list[i].name, \
                'Название товара {} не соответствует API:{}'.format(products.product_list[i].name,
                                                                    products_api.product_list[i].name)
            assert products.product_list[i].description == products_api.product_list[i].description, \
                'Описание товара {} не соответствует API:{}'.format(products.product_list[i].description,
                                                                    products_api.product_list[i].description)
            assert products.product_list[i].price == products_api.product_list[i].price, \
                'Цена товара {} не соответствует API:{}'.format(products.product_list[i].price,
                                                                products_api.product_list[i].price)
            assert products_api.product_list[i].image in products.product_list[i].image, \
                'Изображение товара {} не соответствует API:{}'.format(products.product_list[i].image,
                                                                       products_api.product_list[i].image)



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

        data = self.driver.data
        product = Product()
        data.pre_basket = Basket()
        cheapest_wear = self.search_the_cheapest_product(search_result)
        cheapest_wear.find_element_by_xpath('./td[5]//i[contains(@class, "fa-cart-plus")]').click()
        product.parse(cheapest_wear)
        data.pre_basket.add(product)

        max_price = float(cheapest_wear.find_element_by_xpath('./td[4]').text)
        cheapest_wear = self.search_the_cheapest_product(search_result, max_price)
        cheapest_wear.find_element_by_xpath('./td[5]//i[contains(@class, "fa-cart-plus")]').click()
        product.parse(cheapest_wear)
        data.pre_basket.add(product)

    def search_the_cheapest_product(self, products, max_previous_price=9223372036854775807):
        max_price = 0
        for product in products:
            price = float(product.find_element_by_xpath('./td[4]').text)
            if price > max_price and price < max_previous_price:
                max_price = price
                cheapest_wear = product
        return cheapest_wear
