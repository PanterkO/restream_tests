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
    #request.addfinalizer(fixture.browser_close())
    return fixture

def test_login_in_owasp(driver):

    driver.open_url('https://restream.sloppy.zone')
    driver.login('restream5@mailinator.com','123456')

    time.sleep(.5)
    search_result = driver.search_product('OWASP')
    driver.assert_result(search_result)
    driver.add_the_cheapest_product_in_basket(search_result)
    driver.check_products_in_basket()
    time.sleep(10)
