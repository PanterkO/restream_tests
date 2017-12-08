
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, login, password):

        driver = self.driver.wd
        driver.find_element_by_xpath('//a[@href="#/login"]').click()
        login_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userEmail"]')))
        login_field.send_keys(login)
        password_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userPassword"]')))
        password_field.send_keys(password)
        login_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginButton"]')))
        login_btn.click()
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="loginButton"]')))