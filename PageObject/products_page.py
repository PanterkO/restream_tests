import time


class ProductsPage:
    def __init__(self, driver):
        self.driver = driver

    def search_product(self, product):
        #with open(os.getcwd()+'/script.js') as script:
        #    self.wd.execute_script(script.read())
        self.driver.wd.find_element_by_xpath('//nav//input[@ng-model="searchQuery"]').send_keys(product)
        self.driver.wd.find_element_by_xpath('//*[@id="searchButton"]').click()
        self.driver.data.search_result = self.driver.wd.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')

    def assert_search_result(self, search_result):
        time.sleep(.5)
        # logs = self.wd.get_log('browser')
        # todo -проверить, что на странице содержатся все элементы которые бекэнд вернул на запрос
        # todo -для каждого элемента корректно выводится: название товара, описание товара, картинка на товар и цена
        # todo -для каждого товара есть иконка "посмотреть" (глаз) и "купить (корзина)
        assert len(search_result) == 10

    def assert_every_product_have_icons_show_details_and_add_to_basket(self, products):
        # todo -для каждого товара есть иконка "посмотреть" (глаз) и "купить (корзина)
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

            assert show_details_is_present is True, 'Icon ShowDetails is not found for {}'.format(product.find_element_by_xpath('.//td[2]').text)
            assert add_to_basket_is_present is True, 'Icon AddToBasket is not found for {}'.format(product.find_element_by_xpath('.//td[2]').text)

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