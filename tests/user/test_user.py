import pytest
import src.base.user_utils
import conf

user_utils = src.base.user_utils


def test_create_user(get_random_user_name, get_random_first_name, get_random_last_name):
    assert user_utils.create_user(
        get_random_user_name, get_random_first_name, get_random_last_name).status_code == 200, "User is not created"


def test_check_if_user_exist(get_random_user_name):
    assert user_utils.is_user_exist(get_random_user_name), f"User {get_random_user_name} is not found"


@pytest.mark.parametrize('wrong_user_name, expected_result', [
    ("Don", 404),
    ("Bob", 404),
    ("Bill", 404)
])
def test_check_if_user_exist_negative(wrong_user_name, expected_result):
    assert user_utils.get_user(wrong_user_name).status_code == expected_result, f"User {wrong_user_name} is found"


def test_login_user(get_random_user_name):
    response = user_utils.login_user(get_random_user_name, conf.PASSWORD)

    assert response.status_code == 200
    assert "logged in" in response.json()["message"], "Incorrect login message"


@pytest.mark.parametrize('wrong_password, expected_status_code, expected_message', [
    ("Qwerty", 400, "Invalid username/password supplied"),
    ("Fhgjgig90", 400, "Invalid username/password supplied"),
    ("Irjg889797", 400, "Invalid username/password supplied")
])
def test_login_user_with_wrong_password(get_random_user_name, wrong_password, expected_status_code, expected_message):
    response = user_utils.login_user(get_random_user_name, wrong_password)

    assert response.status_code == expected_status_code, "User logged successfully with wrong password"
    assert response.json()["message"] == expected_message, "Incorrect login message"


@pytest.mark.parametrize('wrong_user_name, expected_status_code, expected_message', [
    ("Bob", 400, "Invalid username/password supplied"),
    ("Dilan", 400, "Invalid username/password supplied"),
    ("Someone", 400, "Invalid username/password supplied")
])
def test_login_user_with_wrong_user_name(wrong_user_name, expected_status_code, expected_message):
    response = user_utils.login_user(wrong_user_name, conf.PASSWORD)

    assert response.status_code == expected_status_code, "User logged successfully with wrong user name"
    assert response.json()["message"] == expected_message, "Incorrect login message"


def test_update_user(get_random_user_name):
    response = user_utils.update_user(get_random_user_name)

    assert response.status_code == 200, "User is not updated"
    assert user_utils.get_user_info(get_random_user_name)["email"] == conf.NEW_USER_EMAIL, "User's email is not updated"


def test_delete_user(get_random_user_name):
    response = user_utils.delete_user(get_random_user_name)

    assert response.status_code == 200, "User is not deleted"
    assert user_utils.get_user(get_random_user_name).status_code == 404, "Uer still exist"


def test_logout_user():
    response = user_utils.logout_user()

    assert response.status_code == 200, "User is not logout"


def test_create_list_of_users():
    users = user_utils.create_users_with_list()[0]
    user_to_check = users[0]["username"]
    response = user_utils.create_users_with_list()[1]

    assert response.status_code == 200, "Users with list are not created"
    assert user_utils.get_user(user_to_check).status_code == 200, "User is not found"

