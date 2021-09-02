"""Store tests related to start page"""

from conftest import BaseTest
from constants.login_page import LoginPageConstants
from helpers.base import UserData


class TestLoginPage(BaseTest):

    def test_successful_login(self, start_page, logout):
        """
        - Fill in fields <username> and <password> and click on Sign In button
        - Verify that login is successful
        """
        # Fill in username and password fields and click on Sign In button
        user_data = UserData(name=LoginPageConstants.REGISTERED_USERNAME,
                             password=LoginPageConstants.REGISTERED_PASSWORD)
        profile_page = start_page.login(user_data)
        self.log.info("Required fields are filled in and Sign In button is pressed")

        # Verify successful login
        profile_page.verify_hello_message(LoginPageConstants.REGISTERED_USERNAME)
        self.log.info("Registered user logged in successfully")

    def test_successful_registration(self, user: UserData, start_page, logout):
        """
        - Fill in registration fields with random valid values and click on Sign Up button
        - Verify success registration
        """
        start_page.register_user(user)
        profile_page = start_page.click_sign_up_and_verify()
        self.log.info("Required fields are filled in and Sign Up button is pressed")

        # Verify success registration
        profile_page.verify_hello_message(user.name)
        self.log.info("Random user registered successfully")

    def test_existing_user_reregistration(self, start_page):
        """
        - Fill in registration fields with existing user data and click on Sign Up button
        - Verify error message
        """
        # Fill in registration field with existing username, email and password and click on Sign Up button
        user = UserData(name=LoginPageConstants.REGISTERED_USERNAME,
                        email=LoginPageConstants.REGISTERED_EMAIL,
                        password=LoginPageConstants.REGISTERED_PASSWORD)
        start_page.register_user(user)
        self.log.info("Required fields are filled in with existing user data and Sign Up button is pressed")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_USERNAME_EXISTS)
        start_page.verify_error_message(text=LoginPageConstants.MSG_EMAIL_EXISTS)
        self.log.info("Error message match to expected")

    def test_short_user_name(self, user: UserData, start_page):
        """
         - Fill in registration form with user data and name less than 3 symbols and click on Sign Up button
         - Verify error message
         """
        # Fill in registration fields
        user.name = user.name[:2]
        start_page.register_user(user)
        self.log.info("Required fields are filled in (<name> is less than 3 symbols) and Sign Up button is pressed")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_USERNAME_MIN_LENGTH)
        self.log.info("Error message match to expected")

    def test_long_user_name(self, user: UserData, start_page):
        """
         - Fill in registration form with user data and name more than 30 symbols and click on Sign Up button
         - Verify error message
         """
        # Fill in registration fields
        user.name = user.name * 3
        start_page.register_user(user)
        self.log.info("Required fields are filled in (<name> is more than 30 symbols) and Sign Up button is pressed")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_USERNAME_MAX_LENGTH)
        self.log.info("Error message match to expected")

    def test_user_name_invalid_char(self, user: UserData, start_page):
        """
         - Fill in registration form with user data and name with non ascii symbols and Sign Up button is pressed
         - Verify error message
         """
        # Fill in registration fields
        user.name = LoginPageConstants.NON_ASCII_USERNAME
        start_page.register_user(user)
        self.log.info("Required fields are filled in (<name> with non ascii symbols) and Sign Up button is pressed")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_USERNAME_ALLOWED_SYMBOLS)
        self.log.info("Error message match to expected")

    def test_existing_email(self, user: UserData, start_page):
        """
        - Fill in registration fields with new user name and existing email and click on Sign Up button
        - Verify error message
        """
        # Fill in registration field with random username and existing email and click on Sign U
        user.email = LoginPageConstants.REGISTERED_EMAIL
        start_page.register_user(user)
        self.log.info("Existing email is used to register new user")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_EMAIL_EXISTS)
        self.log.info("Error message match to expected")

    def test_not_valid_email(self, user: UserData, start_page):
        """
        - Fill in registration fields with random user name and invalid email and click on Sign Up button
        - Verify error message
        """
        # Fill in registration field with random username and existing email and click on Sign U
        user.email = user.email.replace('@', '_')
        start_page.register_user(user)
        self.log.info("Invalid email is used to register new user")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_INVALID_EMAIL)
        self.log.info("Error message match to expected")

    def test_email_prefix_exceed_max_length(self, user: UserData, start_page):
        """
        - Fill in registration fields with random user name and email address with email prefix > 64 symbols
        - Click on Sign Up button
        - Verify error message
        """
        # Fill in registration field with random username and existing email and click on Sign U
        # email prefix should be > 64 symbols to pass test
        user.email = f"{user.name:z>65}@{user.email.split('@')[1]}"
        start_page.register_user(user)
        start_page.click_sign_up_and_verify(element_expected=False)
        self.log.info("Email prefix in email address exceeds max possible length")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_INVALID_EMAIL_LENGTH)
        self.log.info("Error message match to expected")

    def test_email_domain_exceed_max_length(self, user: UserData, start_page):
        """
        - Fill in registration fields with random user name and email address with @domain > 64 symbols
        - Click on Sign Up button
        - Verify error message
        """
        # Fill in registration fields
        # @ and email domain together should be > 64 symbols to pass test
        user.email = f"{user.name}@{user.email.split('@')[1]:z>70}"
        start_page.register_user(user)
        start_page.click_sign_up_and_verify(element_expected=False)
        self.log.info("Domain in email address exceeds max possible length")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_INVALID_EMAIL_LENGTH)
        self.log.info("Error message match to expected")

    def test_short_password(self, user: UserData, start_page):
        """
         - Fill in registration form with user data and password less than 12 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Fill in registration fields
        user.password = user.password[:11]
        start_page.register_user(user)

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_PASSWORD_MIN_LENGTH)
        self.log.info("Error message match to expected")

    def test_long_password(self, user: UserData, start_page):
        """
         - Fill in registration form with user data and password more than 50 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Fill in registration fields
        user.password = user.password * 5
        start_page.register_user(user)
        self.log.info("Required fields are filled in (<password> is longer than 50 symbols)")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_PASSWORD_MAX_LENGTH)
        self.log.info("Error message match to expected")

    def test_empty_fields_login(self, start_page):
        """
        - Clear name and password fields and click on Sign In button
        - Verify error message
        """
        # Clear name and password fields and click on Sign In button
        start_page.login(UserData())
        self.log.info("Log in with empty name and password fields")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_INVALID_LOGIN)
        self.log.info("Error message match to expected")

    def test_invalid_login(self, user: UserData, start_page):
        """
        - Fill in login fields with invalid values and click on Sign In button
        - Verify error message
        """
        # Fill in username and password fields and click on Sign In button
        start_page.login(user)
        self.log.info("Fields are filled in with invalid values")

        # Verify error message
        start_page.verify_error_message(text=LoginPageConstants.MSG_INVALID_LOGIN)
        self.log.info("Error message match to expected")
