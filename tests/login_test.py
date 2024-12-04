import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()


def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open_page(" http://127.0.0.1:8000/login/")
    time.sleep(1)
    login_page.enter_username("user")
    time.sleep(1)
    login_page.enter_password("user")
    time.sleep(1)
    login_page.click_login()
    time.sleep(1)