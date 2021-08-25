import platform


class BaseConstants:
    """Store common constants of test framework"""

    START_PAGE_URL = "https://qa-complex-app-for-testing.herokuapp.com"

    if platform.system() == 'Linux':
        # path to WebDriver for Ubuntu:
        DRIVER_PATH = r"./drivers/chromedriver"
    elif platform.system() == 'Windows':
        # path to WebDriver for Windows:
        DRIVER_PATH = r"./drivers/chromedriver.exe"
    else:
        raise NotImplementedError(f"Path to WebDriver for {platform.system()} is not implemented")
