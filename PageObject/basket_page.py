import time


class BasketPage:

    def __init__(self, driver):
        self.driver = driver

    def check_products_in_basket(self):
        self.driver.wd.find_element_by_xpath('//nav//a[@href="#/basket"]').click()
        basket = self.driver.wd.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
        # todo -проверить что в корзине содержатся два этих товара
        # todo -проверить что их цена в корзине соответствует их цене со страницы поиска
        for product in basket:
            product_name = product.find_element_by_xpath('.//td[1]')
            product_price = product.find_element_by_xpath('.//td[3]')

    def clear_basket(self):
        # fixture для очистки корзины перед тестом
        self.driver.wd.find_element_by_xpath('//nav//a[@href="#/basket"]').click()
        time.sleep(1)
        try:
            basket = self.driver.wd.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
            for product in basket:
                product.find_element_by_xpath('.//i[contains(@class, "fa-trash-o")]').click()
        except Exception:
            print('Basket is empty!')