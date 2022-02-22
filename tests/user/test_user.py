import pytest
from src.utils import get_config
import src.base.user as user_utils
from src.const.status_codes import Statuses as status
from src.const.user_errors import ErrorMessages as errorMes


def test_check_if_user_exist(create_test_user, get_random_user_name):
    assert create_test_user.status_code == status.OK, f"User {get_random_user_name} is not found"


@pytest.mark.parametrize('wrong_user_name, expected_result', [
    ("Don", status.NOT_FOUND),
    ("Bob", status.NOT_FOUND),
    ("Bill", status.NOT_FOUND)
])
def test_check_if_user_exist_negative(wrong_user_name, expected_result):
    assert user_utils.get_user(wrong_user_name).status_code == expected_result, f"User {wrong_user_name} is found"


def test_login_user(create_test_user, get_random_user_name):
    response = user_utils.login_user(get_random_user_name, get_config('Password', 'password'))

    assert response.status_code == status.OK
    assert "logged in" in response.json()["message"], "Incorrect login message"


@pytest.mark.parametrize('wrong_password, expected_status_code, expected_message', [
    ("Qwerty", status.BAD_REQUEST, errorMes.LOGIN_ERROR),
    ("Fhgjgig90", status.BAD_REQUEST, errorMes.LOGIN_ERROR),
    ("Irjg889797", status.BAD_REQUEST, errorMes.LOGIN_ERROR)
])
def test_login_user_with_wrong_password(get_random_user_name, wrong_password, expected_status_code, expected_message):
    response = user_utils.login_user(get_random_user_name, wrong_password)

    assert response.status_code == expected_status_code, "User logged successfully with wrong password"
    assert response.json()["message"] == expected_message, "Incorrect login message"


@pytest.mark.parametrize('wrong_user_name, expected_status_code, expected_message', [
    ("Bob", status.BAD_REQUEST, errorMes.LOGIN_ERROR),
    ("Dilan", status.BAD_REQUEST, errorMes.LOGIN_ERROR),
    ("Someone", status.BAD_REQUEST, errorMes.LOGIN_ERROR)
])
def test_login_user_with_wrong_user_name(wrong_user_name, expected_status_code, expected_message):
    response = user_utils.login_user(wrong_user_name, get_config('Password', 'password'))

    assert response.status_code == expected_status_code, "User logged successfully with wrong user name"
    assert response.json()["message"] == expected_message, "Incorrect login message"


def test_update_user(create_test_user, get_random_user_name):
    user = create_test_user
    response = user_utils.update_user(get_random_user_name)

    assert response.status_code == status.OK, "User is not updated"
    assert user_utils.get_user_info(user)["email"] == get_config('Email', 'new_user_email'), \
        "User's email is not updated"


def test_delete_user(create_test_user, get_random_user_name):
    user = create_test_user
    user_utils.delete_user(get_random_user_name)

    assert user.status_code == status.NOT_FOUND, f"User {get_random_user_name} still exist "


def test_logout_user():
    response = user_utils.logout_user()

    assert response.status_code == status.OK, "User is not logout"


def test_create_list_of_users():
    users = user_utils.create_users_with_list()[0]
    user_to_check = users[0]["username"]
    response = user_utils.create_users_with_list()[1]

    assert response.status_code == status.OK, "Users with list are not created"
    assert user_utils.get_user(user_to_check).status_code == status.OK, "User is not found"
