import logging

from constants.profile_page import ProfilePageConstants
from helpers.base import BaseHelpers


# TODO: multi-inheritance - BaseHelpers, BaseTest
class ProfileHelpers(BaseHelpers):
    """Store helper methods related to Profile Page actions"""

    def __init__(self, driver):
        super().__init__(driver)
        self.log = logging.getLogger(__name__)

    def verify_hello_message(self, username):
        """Find hello message and verify in all possible ways"""

        hello_message = self.driver.find_element_by_tag_name(ProfilePageConstants.HELLO_MSG_TAG_NAME)
        assert username.lower() in hello_message.text
        assert hello_message.text == ProfilePageConstants.HELLO_MSG_TEXT.format(username_lower=username.lower())
        assert self.driver.find_element_by_xpath(ProfilePageConstants.HELLO_MSG_USERNAME_XPATH).text == username.lower()
