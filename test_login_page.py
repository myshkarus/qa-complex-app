"""Store tests related to start page"""

# author: Mykhailo Shpilienko, AUTP_G2
# date:   10-08-2021

from time import sleep

import pytest
from selenium import webdriver
from selenium import common

from conftest import BaseTest
import random
import string

reg_user_name = 'aryastark'
reg_user_password = '20210727Abcd'
reg_user_email = 'aryastark20210727@yahoo.com'

n = 0


class TestLoginPage(BaseTest):

    @pytest.fixture(scope='class')
    def driver(self):

        # path for Ubuntu:
        driver = webdriver.Chrome(executable_path=r"./drivers/chromedriver")

        # TODO: let code decide on OS type
        # path for Windows:
        # driver = webdriver.Chrome(executable_path=r"./drivers/chromedriver.exe")
        yield driver
        driver.close()

    @pytest.fixture(scope='function')
    def random_user(self):
        """Return tuple with random user name, email and password"""
        user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        email = f"{user}@yahoo.com"
        pwd = f"{user}{random.randint(0, 1000)}"
        some_user = user, email, pwd
        yield some_user
        del some_user

    @pytest.fixture(scope='function')
    def log_out(self, driver):
        """Log out logged in user"""
        try:
            logout = driver.find_element_by_xpath(".//button[contains(text(),'Sign Out')]")
            sleep(0.5)
            logout.click()
            sleep(0.5)
        except common.exceptions.NoSuchElementException:
            pass

    @pytest.mark.skip()
    def test_successful_login(self, driver, log_out):
        """
        - Open start page
        - Clear username and password fields
        - Fill in fields <username> and <password>
        - Click on Sign In button
        - Verify login is successful
        """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear username and password fields
        username = driver.find_element_by_xpath(".//input[@placeholder='Username']")
        username.clear()
        password = driver.find_element_by_xpath(".//input[@placeholder='Password']")
        password.clear()
        self.log.info("Fields are cleared")

        # Fill in fields <username> and <password>
        username.send_keys(reg_user_name)
        password.send_keys(reg_user_password)
        self.log.info("Fields <username>, <password> are filled with values of registered user")

        # Click on Sign In button
        sign_in_button = driver.find_element_by_xpath(".//button[contains(text(), 'Sign In')]")
        sleep(1)
        sign_in_button.click()
        self.log.info("Clicked on 'Sign In'")

        # Verify successful login
        sleep(5)
        hello_message = driver.find_element_by_tag_name('h2')
        assert reg_user_name in hello_message.text
        self.log.info("Registered user logged in successfully")

    @pytest.mark.skip()
    def test_successful_registration(self, driver, random_user, log_out):
        """
        - Open start page
        - Clear username, email and password fields in registration form
        - Fill in registration fields with random valid values
        - Click on Sign Up button
        - Verify success registration
        Note: this test should allow to be executed multiple times
        """

        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0])
        email.send_keys(random_user[1])
        password.send_keys(random_user[2])
        self.log.info("Fields <username>, <email>, <password> are filled with valid values")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify success registration
        sleep(1)
        hello_message = driver.find_element_by_tag_name('h2')
        assert random_user[0] in hello_message.text
        self.log.info("Random user registered successfully")

    @pytest.mark.skip()
    def test_existing_user_reregistration(self, driver, log_out):
        """
        - Open start page
        - Clear username, email and password fields in registration form
        - Fill in registration fields with existing user data
        - Click on Sign Up button
        - Verify error message
        """

        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(reg_user_name)
        email.send_keys(reg_user_email)
        password.send_keys("1234567890Qwerty")
        self.log.info("Fields <username>, <email>, <password> are filled with name and email of registered user")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(".//div[contains(text(),'username is already taken')]")
        assert error_message.text == "That username is already taken."
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_existing_email(self, driver, random_user, log_out):
        """
        - Open start page
        - Clear username, email and password fields in registration form
        - Fill in registration fields with random user name and registered email
        - Click on Sign Up button
        - Verify error message
        """

        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0])
        email.send_keys(reg_user_email)
        password.send_keys(random_user[2])
        self.log.info("Required fields are filled in (<email> is already registered)")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify success registration
        sleep(1)
        error_message = driver.find_element_by_xpath(".//div[contains(text(),'email is already being used')]")
        assert error_message.text == "That email is already being used."
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_not_valid_email(self, driver, random_user, log_out):
        """
        - Open start page
        - Clear username, email and password fields in registration form
        - Fill in registration fields with random user name and invalid email
        - Click on Sign Up button
        - Verify error message
        """

        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0])
        email.send_keys(reg_user_email.replace('@', '_'))
        password.send_keys(random_user[2])
        self.log.info("Required fields are filled in (<email> is not valid)")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(
            ".//div[contains(text(),'You must provide a valid email address.')]")
        assert error_message.text == "You must provide a valid email address."
        self.log.info("Error message match to expected")

    def test_email_prefix_exceed_max_length(self, driver, random_user, log_out):
        """
        - Open start page
        - Clear username, email and password fields in registration form
        - Fill in registration fields with random user name and email address with email prefix > 64 symbols
        - Click on Sign Up button
        - Verify error message
        """

        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0])
        # email prefix should be > 64 symbols to pass test
        email.send_keys(f"{random_user[0]:0<65}@yahoo.com")
        password.send_keys(random_user[2])
        self.log.info("Email prefix in email address exceeds max possible length")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(
            ".//div[contains(text(),'You must provide a avalid email address.')]")
        assert error_message.text == "You must provide a avalid email address."
        self.log.info("Error message match to expected")

    def test_email_domain_exceed_max_length(self, driver, random_user, log_out):
        """
        - Open start page
        - Clear username, email and password fields in registration form
        - Fill in registration fields with random user name and email address with @domain > 64 symbols
        - Click on Sign Up button
        - Verify error message
        """

        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0])
        # @ and email domain together should be > 64 symbols to pass test
        email.send_keys(f"{random_user[0]}@{random_user[0]:0<64}.com")
        password.send_keys(random_user[2])
        self.log.info("Domain in email address exceeds max possible length")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(
            ".//div[contains(text(),'You must provide a avalid email address.')]")
        assert error_message.text == "You must provide a avalid email address."
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_short_user_name(self, driver, random_user, log_out):
        """
         - Open start page
         - Clear username, email and password fields in registration form
         - Fill in registration form with user data and name less than 3 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0][:2])
        email.send_keys(random_user[1])
        password.send_keys(random_user[2])
        self.log.info("Required fields are filled in (<name> is less than 3 symbols)")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(
            ".//div[contains(text(),'Username must be at least 3 characters.')]")
        assert error_message.text == "Username must be at least 3 characters."
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_user_name_invalid_char(self, driver, random_user, log_out):
        """
         - Open start page
         - Clear username, email and password fields in registration form
         - Fill in registration form with user data and name with non ascii symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys("Zlatan Ibrahimović")
        email.send_keys(random_user[1])
        password.send_keys(random_user[2])
        self.log.info("Required fields are filled in (<name> contains non ascii symbols)")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(
            ".//div[contains(text(),'Username can only contain letters and numbers.')]")
        assert error_message.text == "Username can only contain letters and numbers."
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_short_password(self, driver, random_user, log_out):
        """
         - Open start page
         - Clear username, email and password fields in registration form
         - Fill in registration form with user data and password less than 12 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0])
        email.send_keys(random_user[1])
        password.send_keys(random_user[2][:11])
        self.log.info("Required fields are filled in (<password> is less than 12 symbols)")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(
            ".//div[contains(text(),'Password must be at least 12 characters.')]")
        assert error_message.text == "Password must be at least 12 characters."
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_long_password(self, driver, random_user, log_out):
        """
         - Open start page
         - Clear username, email and password fields in registration form
         - Fill in registration form with user data and password more than 50 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0])
        email.send_keys(random_user[1])
        password.send_keys(random_user[2] * 5)
        self.log.info("Required fields are filled in (<password> is longer than 50 symbols)")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(".//div[contains(text(),'Password cannot exceed 50 characters')]")
        assert error_message.text == "Password cannot exceed 50 characters"
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_long_user_name(self, driver, random_user, log_out):
        """
         - Open start page
         - Clear username, email and password fields in registration form
         - Fill in registration form with user data and name more than 30 symbols
         - Click on Sign Up button
         - Verify error message
         """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open start page")

        # Clear fields
        username = driver.find_element_by_id("username-register")
        email = driver.find_element_by_id("email-register")
        password = driver.find_element_by_id("password-register")
        username.clear()
        email.clear()
        password.clear()
        self.log.info("Fields <username>, <email>, <password> are cleared")

        # Fill in registration fields
        username.send_keys(random_user[0] * 3)
        email.send_keys(random_user[1])
        password.send_keys(random_user[2])
        self.log.info("Required fields are filled in (<name> is more than 30 symbols)")

        # Click on Sign Up button
        sign_up_button = driver.find_element_by_xpath(".//*[@id='registration-form']/button")

        # без паузы и с очень короткой паузой <1 тест валится
        sleep(1)
        sign_up_button.click()
        self.log.info("Clicked on 'Sign Up' button")

        # Verify error message
        sleep(1)
        error_message = driver.find_element_by_xpath(".//div[contains(text(),'Username cannot exceed 30 characters.')]")
        assert error_message.text == "Username cannot exceed 30 characters."
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_empty_fields_login(self, driver, log_out):
        """
        - Open start page
        - Clear password and login fields
        - Click on Sign In button
        - Verify error message
        """

        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open page")

        # Clear required fields
        username = driver.find_element_by_xpath(".//input[@placeholder='Username']")
        username.clear()
        password = driver.find_element_by_xpath(".//input[@placeholder='Password']")
        password.clear()
        self.log.info("Fields are cleared")

        # Click on Sign In button
        sign_in_button = driver.find_element_by_xpath(".//button[contains(text(), 'Sign In')]")
        sign_in_button.click()
        self.log.info("Clicked on 'Sign In'")

        # Verify error message
        error_message = driver.find_element_by_xpath(".//div[contains(text(),'Invalid username / password')]")
        assert error_message.text == 'Invalid username / password'
        self.log.info("Error message match to expected")

    @pytest.mark.skip()
    def test_invalid_login(self, driver, log_out):
        """
        - Open start page
        - Clear password and login fields
        - Fill in fields with invalid values
        - Click on Sign In button
        - Verify error message
        """

        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open page")

        # Clear required fields and fill in
        username = driver.find_element_by_xpath(".//input[@placeholder='Username']")
        username.clear()
        username.send_keys('TestUser')
        password = driver.find_element_by_xpath(".//input[@placeholder='Password']")
        password.clear()
        password.send_keys('~123Abcd')
        sleep(1)
        self.log.info("Fields are filled in with invalid values")

        # Click on Sign In button
        sign_in_button = driver.find_element_by_xpath(".//button[contains(text(), 'Sign In')]")
        sign_in_button.click()
        self.log.info("Clicked on 'Sign In'")

        # Verify error message
        error_message = driver.find_element_by_xpath(".//div[contains(text(),'Invalid username / password')]")
        assert error_message.text == 'Invalid username / password'
        self.log.info("Error message match to expected")
