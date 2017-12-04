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


def test_login_in_owasp(driver):

    data = driver.data
    driver.open_url(data.url)
    driver.login_page.login(data.login, data.password)
    time.sleep(.5)
    driver.basket.clear_basket()
    time.sleep(.5)
    driver.products_page.search_product(data.search_path)
    driver.products_page.assert_search_result(data.search_result)
    driver.products_page.add_the_cheapest_product_to_basket(data.search_result)
    driver.basket.check_products_in_basket()
    time.sleep(10)
