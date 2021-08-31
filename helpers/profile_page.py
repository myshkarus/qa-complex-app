import logging

from selenium.webdriver.common.by import By

from constants.profile_page import ProfilePageConstants
from helpers.base import BaseHelpers


class ProfileHelpers(BaseHelpers):
    """Store helper methods related to Profile Page actions"""

    def __init__(self, driver):
        super().__init__(driver)
        self.log = logging.getLogger(__name__)

    def verify_hello_message(self, username):
        """Find hello message and verify in all possible ways"""

        self.wait_for_text(locator_type=By.TAG_NAME, locator=ProfilePageConstants.HELLO_MSG_TAG_NAME,
                           text=ProfilePageConstants.HELLO_MSG_TEXT.format(username_lower=username.lower()))
        assert self.wait_until_element_find(locator_type=By.XPATH,
                                            locator=ProfilePageConstants.HELLO_MSG_USERNAME_XPATH).text == username.lower()
