from selenium.webdriver.chrome.webdriver import WebDriver
import time

class Driver:

    def __init__(self):
        self.wd = WebDriver()
        self.wd.maximize_window()
        self.wd.implicitly_wait(60)
       # self.wd.capabilities()


    def browser_close(self):
        self.wd.close()
        self.wd.quit()


    def check_products_in_basket(self):
        self.wd.find_element_by_xpath('//nav//a[@href="#/basket"]').click()
        basket = self.wd.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
        for product in basket:
            product_name = product.find_element_by_xpath('.//td[1]')
            product_price = product.find_element_by_xpath('.//td[3]')


    def add_the_cheapest_product_in_basket(self, search_result):
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


    def assert_result(self, search_result):
        time.sleep(.5)

        assert len(search_result) == 10


    def search_product(self, product):
        self.wd.find_element_by_xpath('//nav//input[@ng-model="searchQuery"]').send_keys(product)
        self.wd.find_element_by_xpath('//*[@id="searchButton"]').click()
        js_script = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
        js_result = self.wd.execute_script(js_script)
        print(js_result)
        #print(self.wd.get_log('browser'))
        search_result = self.wd.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
        return search_result


    def login(self, login, password):
        self.wd.find_element_by_xpath('//a[@href="#/login"]').click()
        time.sleep(.5)
        self.wd.find_element_by_xpath('//*[@id="userEmail"]').send_keys(login)
        self.wd.find_element_by_xpath('//*[@id="userPassword"]').send_keys(password)
        self.wd.find_element_by_xpath('//*[@id="loginButton"]').click()


    def open_url(self, url):
        time.sleep(5)
        wd = self.wd
        wd.get(url)
