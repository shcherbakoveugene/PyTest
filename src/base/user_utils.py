import conf
import requests
import random
import string


def params_create_user(user_name, password, firs_name, last_name):
    params = {"username": f"{user_name}",
              "password": f"{password}",
              "firstName": f"{firs_name}",
              "lastName": f"{last_name}",
              "email": f"{conf.USER_EMAIL}"
              }
    return params


def params_login_user(user_name, password):
    params = {"username": f"{user_name}",
              "password": f"{password}"
              }
    return params


def param_for_update():
    params = {"email": f"{conf.NEW_USER_EMAIL}"}
    return params


def random_user_name():
    return "UserInList_" + "".join(random.choice(string.ascii_letters) for i in range(4))


def get_existing_user_url(user_name):
    url = conf.EXISTING_USER + str(user_name)
    return url


def create_user(user_name, first_name, last_name):
    response = requests.post(url=conf.CREATE_USER,
                             json=params_create_user(user_name, conf.PASSWORD, first_name, last_name))
    return response


def get_user(user_name):
    return requests.get(url=get_existing_user_url(user_name))


def get_user_info(user_name):
    user_info = dict(get_user(user_name).json())
    return user_info


def login_user(user_name, password):
    return requests.get(url=conf.LOGIN_USER, params=params_login_user(user_name, password))


def update_user(user_name):
    return requests.put(url=get_existing_user_url(user_name), json=param_for_update())


def delete_user(user_name):
    return requests.delete(url=get_existing_user_url(user_name))


def logout_user():
    return requests.get(url=conf.LOGOUT_USER)


def list_of_users():
    users = [{"username": f"{random_user_name()}", "password": conf.PASSWORD},
             {"username": f"{random_user_name()}", "password": conf.PASSWORD},
             {"username": f"{random_user_name()}", "password": conf.PASSWORD}
             ]
    return users


def create_users_with_list():
    users = list_of_users()
    response = requests.post(url=conf.CREATE_USER_WITH_LIST, json=users)
    return users, response
