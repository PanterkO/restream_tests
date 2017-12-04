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
def driver():
    fixture = Driver()
    return fixture


def test_find_products_owasp(driver):

    data = driver.data
    products_page = driver.products_page
    basket = driver.basket
    login_page = driver.login_page
    # todo убрать слипы
    driver.open_url(data.url)
    login_page.login(data.login, data.password)
    time.sleep(.5)
    products_page.search_product(data.search_path)
    products_page.assert_search_result()


def test_buy_two_cheapest_product(driver):
    data = driver.data
    products_page = driver.products_page
    basket = driver.basket
    login_page = driver.login_page
    driver.open_url(data.url)
    login_page.login(data.login, data.password)
    time.sleep(.5)
    basket.clear_basket()
    products_page.search_product(data.search_path)
    products_page.assert_every_product_have_icons_show_details_and_add_to_basket(data.search_result)
    products_page.add_the_cheapest_product_to_basket(data.search_result)
    basket.check_products_in_basket()
    time.sleep(10)
