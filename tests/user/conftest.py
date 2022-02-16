import string

import pytest
import random


@pytest.fixture(scope="session")
def get_random_user_name():
    return _random_user_name()


@pytest.fixture(scope="session")
def get_random_first_name():
    return _random_user_first_name()


@pytest.fixture(scope="session")
def get_random_last_name():
    return _random_user_last_name()


def _random_user_name():
    return "TestUser_" + "".join(random.choice(string.ascii_letters) for i in range(5))


def _random_user_first_name():
    return "FirstName_" + "".join(random.choice(string.ascii_letters) for i in range(5))


def _random_user_last_name():
    return "LastName_" + "".join(random.choice(string.ascii_letters) for i in range(5))




