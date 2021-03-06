import logging

from selenium.webdriver.common.by import By

from constants.base import BaseConstants
from constants.login_page import LoginPageConstants
from constants.profile_page import ProfilePageConstants
from helpers.base import BaseHelpers, wait_until_ok, UserData
from pages.profile_page import ProfilePage


class LoginPage(BaseHelpers):
    """Store helper methods related to Login Page actions"""

    def __init__(self, driver):
        super().__init__(driver)
        self.log = logging.getLogger(__name__)
        self.constants = LoginPageConstants

    def login(self, user: UserData):
        """Provide credentials and press Sign In button to login"""

        # Clear and fill required fields
        self.fill_input_field(by=By.XPATH, locator=self.constants.SIGN_IN_USERNAME_XPATH, value=user.name)
        self.fill_input_field(by=By.XPATH, locator=self.constants.SIGN_IN_PASSWORD_XPATH, value=user.password)
        self.log.debug("Fields are filled with invalid values")

        # Click on Sign In button
        self.wait_and_click(locator_type=By.XPATH, locator=self.constants.SIGN_IN_BUTTON_XPATH)
        self.log.info("Clicked on 'Sign In'")
        return ProfilePage(driver=self.driver)

    @wait_until_ok(timeout=10)
    def click_sign_up_and_verify(self, element_expected=True):
        """Click on Sign Up button and verify the result"""

        # Click on Sign Up button
        self.wait_and_click(locator_type=By.XPATH, locator=self.constants.SIGN_UP_BUTTON_XPATH)
        self.log.debug("Sign Up button is not clickable")

        if element_expected:
            self.wait_until_element_find(locator_type=By.XPATH, locator=ProfilePageConstants.SIGN_OUT_BUTTON_XPATH)
            # Verify register success
            assert self.is_element_exists(locator_type=By.XPATH, locator=ProfilePageConstants.SIGN_OUT_BUTTON_XPATH)
        else:
            self.verify_error_message(text=self.constants.MSG_INVALID_EMAIL_LENGTH)
        return ProfilePage(self.driver)

    def register_user(self, user: UserData):
        """Fill registration form fields and press Sign Up button to register new user"""

        # Open start page
        self.driver.get(BaseConstants.START_PAGE_URL)
        self.log.debug("Open page")

        self.fill_input_field(by=By.ID, locator=LoginPageConstants.SIGN_UP_USERNAME_ID, value=user.name)
        self.fill_input_field(by=By.ID, locator=LoginPageConstants.SIGN_UP_EMAIL_ID, value=user.email)
        self.fill_input_field(by=By.ID, locator=LoginPageConstants.SIGN_UP_PASSWORD_ID, value=user.password)
        self.log.debug("Fields are filled with invalid values")

        # return username, email, password
        return ProfilePage(self.driver)

    def verify_error_message(self, text):
        """Find error message and assert text"""
        assert self.is_text_exists(locator_type=By.XPATH, locator=f".//*[contains(text(), '{text}')]", text=text)
