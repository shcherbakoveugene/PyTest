from src.utils import get_config
import requests
import random
import string
from loguru import logger
from src.const.status_codes import Statuses as status


def random_user_name():
    return "UserInList_" + "".join(random.choice(string.ascii_letters) for i in range(4))


def get_existing_user_url(user_name):
    url = get_config('Links', 'existing_user') + str(user_name)

    return url


def create_user(user_name, first_name, last_name):
    logger.debug("Creating new user")
    params = {"username": f"{user_name}",
              "password": f"{get_config('Password', 'password')}",
              "firstName": f"{first_name}",
              "lastName": f"{last_name}",
              "email": f"{get_config('Email', 'user_email')}"
              }

    response = requests.post(url=get_config('Links', 'create_user'), json=params)

    if response.status_code == status.OK:
        logger.debug(f"User {user_name} successfully created")

    return response


def get_user(user_name):
    logger.debug("Getting user")
    return requests.get(url=get_existing_user_url(user_name))


def is_user_exist(user_name):
    return get_user(user_name).status_code == status.OK


def get_user_info(user):
    user_info = dict(user.json())

    return user_info


def login_user(user_name, password):
    logger.debug("Login user")
    params = {"username": f"{user_name}",
              "password": f"{password}"
              }

    return requests.get(url=get_config('Links', 'login_user'), params=params)


def update_user(user_name):
    logger.debug("Updating user")
    params = {"email": f"{get_config('Email', 'new_user_email')}"}

    return requests.put(url=get_existing_user_url(user_name), json=params)


def delete_user(user_name):
    logger.debug("Deleting user")

    if requests.delete(url=get_existing_user_url(user_name)).status_code == 200:
        logger.debug(f"User {user_name} successfully deleted")
        return status.OK
    else:
        logger.debug(f"User {user_name} is not deleted")
        return status.NOT_FOUND


def logout_user():
    logger.debug("Logout")
    return requests.get(url=get_config('Links', 'logout_user'))


def create_users_with_list():
    users = [{"username": f"{random_user_name()}", "password": get_config('Password', 'password')},
             {"username": f"{random_user_name()}", "password": get_config('Password', 'password')},
             {"username": f"{random_user_name()}", "password": get_config('Password', 'password')}
             ]
    logger.debug("Creating users with list")
    response = requests.post(url=get_config('Links', 'create_user_with_list'), json=users)

    return users, response
