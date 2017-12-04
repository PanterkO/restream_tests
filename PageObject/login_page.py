import time


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, login, password):
        self.driver.wd.find_element_by_xpath('//a[@href="#/login"]').click()
        time.sleep(.5)
        self.driver.wd.find_element_by_xpath('//*[@id="userEmail"]').send_keys(login)
        self.driver.wd.find_element_by_xpath('//*[@id="userPassword"]').send_keys(password)
        self.driver.wd.find_element_by_xpath('//*[@id="loginButton"]').click()