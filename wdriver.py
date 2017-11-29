from selenium.webdriver.chrome.webdriver import WebDriver

class Driver:

    def __init__(self):
        self.wd = WebDriver()
        self.wd.implicitly_wait(60)

    def browser_close(self):
        self.wd.close()
        self.wd.quit()
