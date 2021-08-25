"""Store tests related to start page"""

# author: Mykhailo Shpilienko, AUTP_G2
# date:   12-08-2021

from time import sleep

import pytest
from selenium import webdriver

from conftest import BaseTest
from constants.base import BaseConstants
from constants.login_page import LoginPageConstants
from constants.profile_page import ProfilePageConstants
from helpers.base import BaseHelpers
from helpers.login_page import LoginHelpers
from helpers.profile_page import ProfileHelpers


class TestLoginPage(BaseTest):

    @pytest.fixture(scope='class')
    def driver(self):
        driver = webdriver.Chrome(executable_path=BaseConstants.DRIVER_PATH)
        yield driver
        driver.close()

    @pytest.fixture(scope='function')
    def log_out(self, driver):
        """Log out the user"""
        yield
        base_helper = BaseHelpers(driver)
        base_helper.find_by_contains_text(ProfilePageConstants.SIGN_OUT_BUTTON_TEXT, "button").click()
        sleep(1)

    @pytest.fixture(scope='function')
    def register(self, driver):
        login_helper = LoginHelpers(driver)
        registered_user = login_helper.register_user(username=self.variety.user, email=self.variety.email,
                                                     password=self.variety.password)
        login_helper.find_by_contains_text(ProfilePageConstants.SIGN_OUT_BUTTON_TEXT, "button").click()
        sleep(1)
        return registered_user

    def test_successful_login(self, driver, log_out):
        """
        - Open start page
        - Fill in fields <username> and <password> and click on Sign In button
        - Verify that login is successful
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in username and password fields and click on Sign In button
        login_helper = LoginHelpers(driver)
        login_helper.login(username=LoginPageConstants.REGISTERED_USERNAME,
                           password=LoginPageConstants.REGISTERED_PASSWORD)
        self.log.info("Fill in required fields and button Sign In is pressed")

        # Verify successful login
        # sleep(3)
        profile_helper = ProfileHelpers(driver)
        profile_helper.verify_hello_message(LoginPageConstants.REGISTERED_USERNAME)
        self.log.info("Registered user logged in successfully")

    def test_successful_registration(self, driver, log_out):
        """
        - Open start page
        - Fill in registration fields with random valid values and click on Sign Up button
        - Verify success registration
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration field with random username, email and password and click on Sign Up button
        login_helper = LoginHelpers(driver)
        user, _, _ = login_helper.register_user(username=self.variety.user, email=self.variety.email,
                                                password=self.variety.password)
        self.log.info("New user is registered")

        # Verify success registration
        # sleep(1)
        profile_helper = ProfileHelpers(driver)
        profile_helper.verify_hello_message(user)
        self.log.info("Random user registered successfully")

    def test_existing_user_reregistration(self, driver):
        """
        - Open start page
        - Fill in registration fields with existing user data
        - Click on Sign Up button
        - Verify error message
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration field with existing username, email and password and click on Sign Up button
        login_helper = LoginHelpers(driver)
        login_helper.register_user(username=LoginPageConstants.REGISTERED_USERNAME,
                                   email=LoginPageConstants.REGISTERED_EMAIL,
                                   password=LoginPageConstants.REGISTERED_PASSWORD)
        self.log.info("Existing user registers")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_USERNAME_EXISTS)
        login_helper.verify_error_message(text=LoginPageConstants.MSG_EMAIL_EXISTS)
        self.log.info("Error message match to expected")

    def test_short_user_name(self, driver):
        """
         - Open start page
         - Fill in registration form with user data and name less than 3 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration fields
        login_helper = LoginHelpers(driver)
        login_helper.register_user(username=self.variety.user[:2], email=self.variety.email,
                                   password=self.variety.password)
        self.log.info("Required fields are filled in (<name> is less than 3 symbols)")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_USERNAME_MIN_LENGTH)
        self.log.info("Error message match to expected")

    def test_long_user_name(self, driver):
        """
         - Open start page
         - Fill in registration form with user data and name more than 30 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration fields
        login_helper = LoginHelpers(driver)
        login_helper.register_user(username=self.variety.user * 3, email=self.variety.email,
                                   password=self.variety.password)
        self.log.info("Required fields are filled in (<name> is more than 30 symbols)")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_USERNAME_MAX_LENGTH)
        self.log.info("Error message match to expected")

    def test_user_name_invalid_char(self, driver):
        """
         - Open start page
         - Fill in registration form with user data and name with non ascii symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration fields
        login_helper = LoginHelpers(driver)
        login_helper.register_user(username=LoginPageConstants.NON_ASCII_USERNAME, email=self.variety.email,
                                   password=self.variety.password)

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_USERNAME_ALLOWED_SYMBOLS)
        self.log.info("Error message match to expected")

    def test_existing_email(self, driver):
        """
        - Open start page
        - Fill in registration fields with new user name and existing email
        - Click on Sign Up button
        - Verify error message
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration field with random username and existing email and click on Sign U
        login_helper = LoginHelpers(driver)
        login_helper.register_user(username=self.variety.user, email=LoginPageConstants.REGISTERED_EMAIL,
                                   password=self.variety.password)
        self.log.info("Existing email is used to register new user")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_EMAIL_EXISTS)
        self.log.info("Error message match to expected")

    def test_not_valid_email(self, driver):
        """
        - Open start page
        - Clear username, email and password fields in registration form
        - Fill in registration fields with random user name and invalid email
        - Click on Sign Up button
        - Verify error message
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration field with random username and existing email and click on Sign U
        login_helper = LoginHelpers(driver)
        login_helper.register_user(username=self.variety.user,
                                   email=LoginPageConstants.REGISTERED_EMAIL.replace('@', '_'),
                                   password=self.variety.password)
        self.log.info("Invalid email is used to register new user")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_INVALID_EMAIL)
        self.log.info("Error message match to expected")

    def test_email_prefix_exceed_max_length(self, driver):
        """
        - Open start page
        - Fill in registration fields with random user name and email address with email prefix > 64 symbols
        - Click on Sign Up button
        - Verify error message
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration field with random username and existing email and click on Sign U
        login_helper = LoginHelpers(driver)
        # email prefix should be > 64 symbols to pass test
        login_helper.register_user(username=self.variety.user,
                                   email=f"{self.variety.email.split('@')[0]:z>65}@{self.variety.email.split('@')[1]}",
                                   password=self.variety.password)
        self.log.info("Email prefix in email address exceeds max possible length")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_INVALID_EMAIL_LENGTH)
        self.log.info("Error message match to expected")

    def test_email_domain_exceed_max_length(self, driver):
        """
        - Open start page
        - Fill in registration fields with random user name and email address with @domain > 64 symbols
        - Click on Sign Up button
        - Verify error message
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration fields
        login_helper = LoginHelpers(driver)
        # @ and email domain together should be > 64 symbols to pass test
        login_helper.register_user(username=self.variety.user,
                                   email=f"{self.variety.email.split('@')[0]}@{self.variety.email.split('@')[1]:z>68}",
                                   password=self.variety.password)
        self.log.info("Domain in email address exceeds max possible length")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_INVALID_EMAIL_LENGTH)
        self.log.info("Error message match to expected")

    def test_short_password(self, driver):
        """
         - Open start page
         - Fill in registration form with user data and password less than 12 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration fields
        login_helper = LoginHelpers(driver)
        login_helper.register_user(username=self.variety.user, email=self.variety.email,
                                   password=self.variety.password[:11])
        self.log.info("Required fields are filled in (<password> is less than 12 symbols)")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_PASSWORD_MIN_LENGTH)
        self.log.info("Error message match to expected")

    def test_long_password(self, driver):
        """
         - Open start page
         - Fill in registration form with user data and password more than 50 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open start page")

        # Fill in registration fields
        login_helper = LoginHelpers(driver)
        login_helper.register_user(username=self.variety.user, email=self.variety.email,
                                   password=self.variety.password * 5)
        self.log.info("Required fields are filled in (<password> is longer than 50 symbols)")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_PASSWORD_MAX_LENGTH)
        self.log.info("Error message match to expected")

    def test_empty_fields_login(self, driver):
        """
        - Open start page
        - Clear name and password fields
        - Click on Sign In button
        - Verify error message
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open page")

        # Clear name and password fields and click on Sign In button
        login_helper = LoginHelpers(driver)
        login_helper.login()
        self.log.info("Log in with empty name and password fields")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_INVALID_LOGIN)
        self.log.info("Error message match to expected")

    def test_invalid_login(self, driver):
        """
        - Open start page
        - Fill in login fields with invalid values and click on Sign In button
        - Verify error message
        """
        # Open start page
        driver.get(BaseConstants.START_PAGE_URL)
        self.log.info("Open page")

        # Fill in username and password fields and click on Sign In button
        login_helper = LoginHelpers(driver)
        login_helper.login(username=self.variety.user, password=self.variety.password)
        self.log.info("Fields are filled in with invalid values")

        # Verify error message
        login_helper.verify_error_message(text=LoginPageConstants.MSG_INVALID_LOGIN)
        self.log.info("Error message match to expected")
