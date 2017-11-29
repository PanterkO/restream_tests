import pytest
from selenium import webdriver
import time
from wdriver import Driver

'''Есть интернет-магазин https://restream.sloppy.zone (логин restream5@mailinator.com \  пароль: 123456)

Нужно покрыть в нем автотестами следующую функциональность:
1. Авторизоваться и выполнить поиск по слову "OWASP", убедиться что результаты поиска выводятся в соответствии с тем что вернул бекэнд
-проверить, что на странице содержатся все элементы которые бекэнд вернул на запрос
-для каждого элемента корректно выводится: название товара, описание товара, картинка на товар и цена
-для каждого товара есть иконка "посмотреть" (глаз) и "купить (корзина)
2. Добавить два самых дорогих товара в корзину (два самых дорогих товара найденных поиском по слову "OWASP")
-проверить что в корзине содержатся два этих товара
-проверить что их цена в корзине соответствует их цене со страницы поиска'''

@pytest.fixture
def driver(request):
    fixture = Driver()
    request.addfinalizer(fixture.browser_close())
    return fixture

def test_login_in_owasp(driver):

    open_url('https://restream.sloppy.zone')
    login('restream5@mailinator.com','123456')

    time.sleep(.5)
    search_result=search_product()
    assert_result(search_result)
    add_the_cheapest_product_in_basket(search_result)
    check_products_in_basket()
    time.sleep(10)


def check_products_in_basket():
    driver.find_element_by_xpath('//nav//a[@href="#/basket"]').click()
    basket = driver.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
    for product in basket:
        product_name = product.find_element_by_xpath('.td[1]')
        product_price = product.find_element_by_xpath('.td[3]')


def add_the_cheapest_product_in_basket(search_result):
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
            cheapest_wear = result
    cheapest_wear.find_element_by_xpath('./td[5]//i[contains(@class, "fa-cart-plus")]').click()


def assert_result(search_result):
    time.sleep(.5)

    assert len(search_result) == 10
    return search_result


def search_product(product='OWASP'):
    driver.find_element_by_xpath('//nav//input[@ng-model="searchQuery"]').send_keys(owasp)
    driver.find_element_by_xpath('//*[@id="searchButton"]').click()
    search_result = driver.find_elements_by_xpath('//tbody/tr[@class="ng-scope"]')
    return search_result


def login(login, password):
    driver.find_element_by_xpath('//a[@href="#/login"]').click()
    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(login)
    driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginButton"]').click()


def open_url(url):
    driver.get(url)
