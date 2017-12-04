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

    def add_the_cheapest_product_to_basket(self, search_result):
        max_price = 0
        cheapest_wear = None
        for result in search_result:
            price = result.find_element_by_xpath('./td[4]')
            if float(price.text) > max_price:
                max_price = float(price.text)
                cheapest_wear = result
        cheapest_wear.find_element_by_xpath('./td[5]//i[contains(@class, "fa-cart-plus")]').click()
        max_price = 0
        for result in search_result:
            price = result.find_element_by_xpath('./td[4]')
            if float(price.text) > max_price and result != cheapest_wear:
                max_price = float(price.text)
                cheapest_wear2 = result
        cheapest_wear2.find_element_by_xpath('./td[5]//i[contains(@class, "fa-cart-plus")]').click()