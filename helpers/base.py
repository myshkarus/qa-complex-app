import logging
import random
import string
import time
from collections import namedtuple

import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def wait_until_ok(timeout, period=0.25):
    """Decorator function"""

    def actual_decorator(target_func):
        logger = logging.getLogger(__name__)

        def wrapper(*args, **kwargs):
            must_end = time.time() + timeout
            while True:
                try:
                    return target_func(*args, **kwargs)
                except (WebDriverException, AssertionError, TimeoutException) as error:
                    error_name = error if str(error) else error.__class__.__name__
                    logger.debug("Catch %s. Left %s seconds", error_name, (must_end - time.time()))
                    if time.time() >= must_end:
                        logger.warning("Waiting timed out after %s", timeout)
                        raise error
                    time.sleep(period)

        return wrapper

    return actual_decorator


class BaseHelpers:
    """Store base helpers of test framework"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=5)

    def is_element_exists(self, locator_type, locator):
        """Check if element exists; return Boolean"""
        try:
            self.wait_until_element_find(locator_type, locator)
        except TimeoutException:
            return False
        return True

    def is_text_exists(self, locator_type, locator, text):
        """Check if text present; return Boolean"""
        try:
            self.wait_for_text(locator_type, locator, text)
        except TimeoutException:
            return False
        return True

    def wait_until_element_find(self, locator_type, locator):
        """Wait until element is found and return it"""
        self.wait.until(EC.presence_of_element_located((locator_type, locator)))
        return self.driver.find_element(by=locator_type, value=locator)

    def wait_and_click(self, locator_type, locator):
        """Wait until element is clickable and click it"""
        self.wait.until(EC.element_to_be_clickable((locator_type, locator)))
        return self.driver.find_element(by=locator_type, value=locator).click()

    def wait_for_text(self, locator_type, locator, text):
        """Wait until text appear on page"""
        self.wait.until(EC.text_to_be_present_in_element((locator_type, locator), text))

    def fill_input_field(self, by, locator, value=""):
        """Find required element using by.X model, clear input field and enter the value"""
        field = self.wait_until_element_find(locator_type=by, locator=locator)
        field.clear()
        field.send_keys(value)

    def find_by_contains_text(self, text, element_tag="*"):
        """Find element using XPATH contains function by text"""
        return self.wait_until_element_find(locator_type=By.XPATH,
                                            locator=f".//{element_tag}[contains(text(), '{text}')]")


class UserData:
    """Store user data used for Sign In and Sign Up forms"""

    def __init__(self, name="", email="", password=""):
        self.name = name
        self.email = email
        self.password = password


def random_user():
    """Return namedtuple with random user name, email and password"""
    RandomUser = namedtuple('RandomUser', ['name', 'email', 'password'])
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    email = f"{name}@domain.com"
    pwd = f"{name}{random.randint(0, 1000)}"
    return RandomUser(name, email, pwd)
