import selenium
import time

class BasePage():

    def __init__(self, driver):
        self.driver = driver


    def find_element_by(self, by, locator):
        element = self.driver.find_element(by, locator)
        return element

    def element_click(self, element):
        element.click()
