from django.test import TestCase

import time
from decimal import Decimal

from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from django.contrib.auth.models import User

from selenium.webdriver.support.select import Select


class ShopTest(LiveServerTestCase):

    def test_auth(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/login/")]').click()

        input_username = selenium.find_element(by='name', value="username")
        input_password = selenium.find_element(by='name', value="password")

        input_username.send_keys("admin")
        input_password.send_keys('1111')

        selenium.find_element(value="Login").click()

        assert 'Hello admin' in selenium.page_source


    def test_registr(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/register/")]').click()

        input_username = selenium.find_element(by='name', value="username")
        input_email = selenium.find_element(by='name', value="email")
        input_password1 = selenium.find_element(by='name', value="password1")
        input_password2 = selenium.find_element(by='name', value="password2")

        input_username.send_keys('test')
        input_email.send_keys('test@gmail.com')
        input_password1.send_keys('test12345678')
        input_password2.send_keys('test12345678')

        selenium.find_element(value="Register").click()

        assert 'Login' in selenium.page_source

    def test_choose_product(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")
        selenium.find_element_by_xpath('//a[contains(@href,"/2/")]').click()

        assert 'Женская толстовка «Олень с подарком»' in selenium.page_source

    def test_to_cart_with_index(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element(by='id', value=2).click()

        lblCartCount = int(selenium.find_element(value='lblCartCount').text)

        assert lblCartCount != 0

    def test_to_cart_with_product_page(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/2/")]').click()
        selenium.find_element(by='id', value=2).click()

        lblCartCount = int(selenium.find_element(value='lblCartCount').text)

        assert lblCartCount != 0

    def test_comment(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/login/")]').click()

        input_username = selenium.find_element(by='name', value="username")
        input_password = selenium.find_element(by='name', value="password")

        input_username.send_keys("admin")
        input_password.send_keys('1111')

        selenium.find_element(value="Login").click()

        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/2/")]').click()

        input_comment = selenium.find_element(by="id", value="30")
        input_comment.send_keys('test')

        selenium.find_element(by="id", value="40").click()

        assert 'test' in selenium.page_source

    def test_add_product(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/login/")]').click()

        input_username = selenium.find_element(by='name', value="username")
        input_password = selenium.find_element(by='name', value="password")

        input_username.send_keys("admin")
        input_password.send_keys('1111')

        selenium.find_element(value="Login").click()

        selenium.get("http://127.0.0.1:8000/admin/mainapp/product/add/")

        selenium.find_element(by='name', value="name").send_keys('test_product')
        selenium.find_element(by='name', value="price").send_keys('1')
        selenium.find_element(by='name', value="description").send_keys('test')
        selenium.find_element(by='name', value="_save").click()

        assert 'test_product' in selenium.page_source

    def test_change_product(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/login/")]').click()

        input_username = selenium.find_element(by='name', value="username")
        input_password = selenium.find_element(by='name', value="password")

        input_username.send_keys("admin")
        input_password.send_keys('1111')

        selenium.find_element(value="Login").click()

        selenium.get("http://127.0.0.1:8000/admin/mainapp/product/15/change/")

        selenium.find_element(by='name', value="name").send_keys('test_product_changed')
        selenium.find_element(by='name', value="_save").click()

        assert 'test_product_changed' in selenium.page_source

    def test_delete_product(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/login/")]').click()

        input_username = selenium.find_element(by='name', value="username")
        input_password = selenium.find_element(by='name', value="password")

        input_username.send_keys("admin")
        input_password.send_keys('1111')

        selenium.find_element(value="Login").click()

        selenium.get("http://127.0.0.1:8000/admin/mainapp/product/15/delete/")
        selenium.find_element(by='xpath', value="//input[@type='submit']").click()

        assert 'test_product_changed' not in selenium.page_source
