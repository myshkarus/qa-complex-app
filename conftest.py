import logging
import random
import string
from collections import namedtuple


def random_user():
    """Return namedtuple with random user name, email and password"""
    RandomUser = namedtuple('RandomUser', ['user', 'email', 'password'])
    user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    email = f"{user}@domain.com"
    pwd = f"{user}{random.randint(0, 1000)}"
    return RandomUser(user, email, pwd)


def pytest_runtest_setup(item):
    item.cls.log = logging.getLogger(item.name)
    item.cls.variety = random_user()


class BaseTest:
    log = logging.getLogger(__name__)
    variety = random_user()
