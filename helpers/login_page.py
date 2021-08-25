import logging
from time import sleep

from selenium.webdriver.common.by import By

from constants.base import BaseConstants
from constants.login_page import LoginPageConstants
from helpers.base import BaseHelpers


# TODO: multi-inheritance - BaseHelpers, BaseTest
class LoginHelpers(BaseHelpers):
    """Store helper methods related to Login Page actions"""

    def __init__(self, driver):
        super().__init__(driver)
        self.log = logging.getLogger(__name__)

    def login(self, username="", password=""):
        """Provide credentials and press Sign In button to login"""

        # Clear and fill required fields
        self.fill_input_field(by=By.XPATH, locator=LoginPageConstants.SIGN_IN_USERNAME_XPATH, value=username)
        self.fill_input_field(by=By.XPATH, locator=LoginPageConstants.SIGN_IN_PASSWORD_XPATH, value=password)
        # TODO: get the log string sorted
        self.log.debug("Fields are filled with invalid values")

        # Click on Sign In button
        self.find_by_contains_text(text=LoginPageConstants.SIGN_IN_BUTTON_TEXT, element_tag="button").click()
        self.log.info("Clicked on 'Sign In'")

        # TODO: sleep(1)

    def register_user(self, username="", email="", password=""):
        """Fill registration form fields and press Sign Up button to register new user"""

        # Open start page
        # TODO: move to __init__
        self.driver.get(BaseConstants.START_PAGE_URL)
        self.log.debug("Open page")

        self.fill_input_field(by=By.ID, locator=LoginPageConstants.SIGN_UP_USERNAME_ID, value=username)
        self.fill_input_field(by=By.ID, locator=LoginPageConstants.SIGN_UP_EMAIL_ID, value=email)
        self.fill_input_field(by=By.ID, locator=LoginPageConstants.SIGN_UP_PASSWORD_ID, value=password)
        self.log.debug("Fields were filled")
        sleep(1)

        # TODO: event click on Sign Up button
        # Click on Sign Up button
        self.driver.find_element_by_xpath(LoginPageConstants.SIGN_UP_BUTTON_XPATH).click()
        sleep(1)

        return username, email, password

    def verify_error_message(self, text):
        """Find error message and assert text"""
        error_message = self.find_by_contains_text(text)
        assert error_message.text == text
