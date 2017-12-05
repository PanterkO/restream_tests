import time

from models.data import Product, Basket


class BasketPage:

    def __init__(self, driver):
        self.driver = driver

    def check_products_in_basket(self):
        data = self.driver.data
        driver = self.driver.wd
        basket = Basket()
        self.driver.wd.find_element_by_xpath('//nav//a[@href="#/basket"]').click()
        basket_elm = self.driver.wd.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
        for product_elm in basket_elm:
            product = Product()
            product.name = product_elm.find_element_by_xpath('.//td[1]').text
            product.price = float(product_elm.find_element_by_xpath('.//td[3]').text)
            product.description = product_elm.find_element_by_xpath('.//td[2]').text
            basket.add(product)
        assert len(basket_elm) == len(data.pre_basket.product_list)

        for i in range(0, len(basket.product_list) - 1):
            assert data.pre_basket.product_list[i].name in driver.page_source, \
                'Название товара {} не найдено в корзине.'.format(data.pre_basket.product_list[i].name)
            assert data.pre_basket.product_list[i].description in driver.page_source, \
                'Описание товара {} не найдено в корзине.'.format(data.pre_basket.product_list[i].description)
            assert str(data.pre_basket.product_list[i].price) in driver.page_source, \
                'Цена товара {} не найдено в корзине.'.format(data.pre_basket.product_list[i].price)

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