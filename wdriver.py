from selenium import webdriver

import time

from PageObject.basket_page import BasketPage
from PageObject.login_page import LoginPage
from PageObject.products_page import ProductsPage
from models.data import TestData


class Driver:

    def __init__(self):
        self.wd = webdriver.Chrome()
        self.wd.maximize_window()
        self.wd.implicitly_wait(1)
        self.data = TestData()
        self.basket = BasketPage(self)
        self.products_page = ProductsPage(self)
        self.login_page = LoginPage(self)

    def open_url(self, url):
        time.sleep(5)
        wd = self.wd
        wd.get(url)

    def execute_js(self, script):
        exec_result = self.wd.execute_script(script)
        return exec_result

    def browser_close(self):
        self.wd.quit()