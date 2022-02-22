import string

import pytest
import random
from src.base.user import create_user, delete_user, is_user_exist, get_user


@pytest.fixture(scope="session")
def create_test_user(get_random_user_name, get_random_first_name, get_random_last_name):
    create_user(get_random_user_name, get_random_first_name, get_random_last_name)
    user = get_user(get_random_user_name)
    yield user
    if is_user_exist:
        delete_user(get_random_user_name)


@pytest.fixture(scope="session")
def get_random_user_name():
    return random_user_name()


@pytest.fixture(scope="session")
def get_random_first_name():
    return random_user_first_name()


@pytest.fixture(scope="session")
def get_random_last_name():
    return random_user_last_name()


def random_user_name():
    return "TestUser_" + "".join(random.choice(string.ascii_letters) for i in range(5))


def random_user_first_name():
    return "FirstName_" + "".join(random.choice(string.ascii_letters) for i in range(5))


def random_user_last_name():
    return "LastName_" + "".join(random.choice(string.ascii_letters) for i in range(5))




