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
        #options.add_argument('headless')
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C:\\Users\\NULS\\PycharmProjects\\ClothingShop\\shop\\static\\chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/login/")]').click()

        input_username = selenium.find_element(by='name',value="username")
        input_password = selenium.find_element(by='name',value="password")

        input_username.send_keys("admin")
        input_password.send_keys('1111')

        selenium.find_element(value="Login").click()

        selenium.get("http://127.0.0.1:8000/admin/")

        time.sleep(5)

