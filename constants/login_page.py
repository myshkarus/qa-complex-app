class LoginPageConstants:
    """Store constants related to Login Page"""

    # Sign In
    SIGN_IN_USERNAME_XPATH = ".//input[@placeholder='Username']"
    SIGN_IN_PASSWORD_XPATH = ".//input[@placeholder='Password']"
    SIGN_IN_BUTTON_TEXT = "Sign In"
    SIGN_IN_BUTTON_XPATH = f".//button[contains(text(), '{SIGN_IN_BUTTON_TEXT}')]"

    # Sign Up
    SIGN_UP_USERNAME_ID = "username-register"
    SIGN_UP_EMAIL_ID = "email-register"
    SIGN_UP_PASSWORD_ID = "password-register"
    # SIGN_UP_BUTTON_TEXT = "Sign up for OurApp"
    SIGN_UP_BUTTON_XPATH = ".//*[@id='registration-form']/button"
    # SIGN_UP_BUTTON_XPATH = f".//button[contains(text(), '{SIGN_UP_BUTTON_TEXT}')]"

    # Messages / alerts
    MSG_INVALID_LOGIN = "Invalid username / password"
    MSG_USERNAME_EXISTS = "That username is already taken."
    MSG_USERNAME_MIN_LENGTH = "Username must be at least 3 characters."
    MSG_USERNAME_MAX_LENGTH = "Username cannot exceed 30 characters."
    MSG_USERNAME_ALLOWED_SYMBOLS = "Username can only contain letters and numbers."
    MSG_PASSWORD_MIN_LENGTH = "Password must be at least 12 characters."
    MSG_PASSWORD_MAX_LENGTH = "Password cannot exceed 50 characters"
    MSG_EMAIL_EXISTS = "That email is already being used."
    MSG_INVALID_EMAIL = "You must provide a valid email address."
    MSG_INVALID_EMAIL_LENGTH = "You must provide a avalid email address."

    # Auxiliary
    REGISTERED_USERNAME = 'aryastark'
    REGISTERED_EMAIL = 'aryastark20210727@yahoo.com'
    REGISTERED_PASSWORD = '20210727Abcd'
    NON_ASCII_USERNAME = "Zlatan Ibrahimović"