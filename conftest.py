import logging

import pytest
from selenium import webdriver

from constants.base import BaseConstants
from helpers.base import UserData, random_user
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


def pytest_runtest_setup(item):
    item.cls.log = logging.getLogger(item.name)
    item.cls.variety = random_user()


class BaseTest:
    log = logging.getLogger(__name__)
    variety = random_user()


@pytest.fixture(scope='class')
def driver():
    driver = webdriver.Chrome(executable_path=BaseConstants.DRIVER_PATH)
    yield driver
    driver.close()


@pytest.fixture(scope='function')
def start_page(driver):
    driver.get(BaseConstants.START_PAGE_URL)
    return LoginPage(driver)


@pytest.fixture(scope='function')
def logout(driver):
    """Log out the user"""
    yield
    ProfilePage(driver).logout()


@pytest.fixture(scope='function')
def user():
    new_user = random_user()
    return UserData(name=new_user.name, email=new_user.email, password=new_user.password)
