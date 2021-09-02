import logging

from selenium.webdriver.common.by import By

import pages.login_page as LP
from constants.profile_page import ProfilePageConstants
from helpers.base import BaseHelpers


class ProfilePage(BaseHelpers):
    """Store helper methods related to Profile Page actions"""

    def __init__(self, driver):
        super().__init__(driver)
        self.log = logging.getLogger(__name__)
        self.constants = ProfilePageConstants

    def logout(self):
        """Click on Log Out button"""
        self.wait_and_click(locator_type=By.XPATH, locator=self.constants.SIGN_OUT_BUTTON_XPATH)
        return LP.LoginPage(self.driver)

    def verify_hello_message(self, username):
        """Find hello message and verify in all possible ways"""

        self.wait_for_text(locator_type=By.TAG_NAME, locator=self.constants.HELLO_MSG_TAG_NAME,
                           text=self.constants.HELLO_MSG_TEXT.format(username_lower=username.lower()))
        assert self.wait_until_element_find(locator_type=By.XPATH,
                                            locator=self.constants.HELLO_MSG_USERNAME_XPATH).text == username.lower()
