import pytest
from src.utils import get_config
import src.base.user as user_utils
from src.enums.status_codes import Statuses as status
from src.enums.user_errors import ErrorMessages as errorMes


def test_create_user(get_random_user_name, get_random_first_name, get_random_last_name):
    assert user_utils.create_user(
        get_random_user_name, get_random_first_name, get_random_last_name).status_code == status.OK.value, \
        "User is not created"


def test_check_if_user_exist(get_random_user_name):
    assert user_utils.is_user_exist(get_random_user_name), f"User {get_random_user_name} is not found"


@pytest.mark.parametrize('wrong_user_name, expected_result', [
    ("Don", status.NOT_FOUND.value),
    ("Bob", status.NOT_FOUND.value),
    ("Bill", status.NOT_FOUND.value)
])
def test_check_if_user_exist_negative(wrong_user_name, expected_result):
    assert user_utils.get_user(wrong_user_name).status_code == expected_result, f"User {wrong_user_name} is found"


def test_login_user(get_random_user_name):
    response = user_utils.login_user(get_random_user_name, get_config('Password', 'password'))

    assert response.status_code == status.OK.value
    assert "logged in" in response.json()["message"], "Incorrect login message"


@pytest.mark.parametrize('wrong_password, expected_status_code, expected_message', [
    ("Qwerty", status.BAD_REQUEST.value, errorMes.LOGIN_ERROR.value),
    ("Fhgjgig90", status.BAD_REQUEST.value, errorMes.LOGIN_ERROR.value),
    ("Irjg889797", status.BAD_REQUEST.value, errorMes.LOGIN_ERROR.value)
])
def test_login_user_with_wrong_password(get_random_user_name, wrong_password, expected_status_code, expected_message):
    response = user_utils.login_user(get_random_user_name, wrong_password)

    assert response.status_code == expected_status_code, "User logged successfully with wrong password"
    assert response.json()["message"] == expected_message, "Incorrect login message"


@pytest.mark.parametrize('wrong_user_name, expected_status_code, expected_message', [
    ("Bob", status.BAD_REQUEST.value, errorMes.LOGIN_ERROR.value),
    ("Dilan", status.BAD_REQUEST.value, errorMes.LOGIN_ERROR.value),
    ("Someone", status.BAD_REQUEST.value, errorMes.LOGIN_ERROR.value)
])
def test_login_user_with_wrong_user_name(wrong_user_name, expected_status_code, expected_message):
    response = user_utils.login_user(wrong_user_name, get_config('Password', 'password'))

    assert response.status_code == expected_status_code, "User logged successfully with wrong user name"
    assert response.json()["message"] == expected_message, "Incorrect login message"


def test_update_user(get_random_user_name):
    response = user_utils.update_user(get_random_user_name)

    assert response.status_code == status.OK.value, "User is not updated"
    assert user_utils.get_user_info(get_random_user_name)["email"] == get_config('Email', 'new_user_email'), \
        "User's email is not updated"


def test_delete_user(get_random_user_name):
    response = user_utils.delete_user(get_random_user_name)

    assert response.status_code == status.OK.value, "User is not deleted"
    assert user_utils.get_user(get_random_user_name).status_code == status.NOT_FOUND.value, "Uer still exist"


def test_logout_user():
    response = user_utils.logout_user()

    assert response.status_code == status.OK.value, "User is not logout"


def test_create_list_of_users():
    users = user_utils.create_users_with_list()[0]
    user_to_check = users[0]["username"]
    response = user_utils.create_users_with_list()[1]

    assert response.status_code == status.OK.value, "Users with list are not created"
    assert user_utils.get_user(user_to_check).status_code == status.OK.value, "User is not found"

