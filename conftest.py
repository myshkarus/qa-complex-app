import logging


def pytest_runtest_setup(item):
    item.cls.log = logging.getLogger(item.name)


class BaseTest:
    log = logging.getLogger(__name__)
