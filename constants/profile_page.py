class ProfilePageConstants:
    """Store constants related to Profile Page"""

    HELLO_MSG_TAG_NAME = "h2"
    HELLO_MSG_TEXT = "Hello {username_lower}, your feed is empty."
    HELLO_MSG_USERNAME_XPATH = ".//strong"
    SIGN_OUT_BUTTON_TEXT = "Sign Out"
    SIGN_OUT_BUTTON_XPATH = f".//button[contains(text(), '{SIGN_OUT_BUTTON_TEXT}')]"
