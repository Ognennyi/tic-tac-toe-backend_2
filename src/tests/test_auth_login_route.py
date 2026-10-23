from uuid import uuid4

from app import app, container


def test_login_success():
    client = app.test_client()

    login = f"test_{uuid4().hex}"
    password = "correct_password"

    signup_response = client.post(
        "/auth/signup",
        json={
            "login": login,
            "password": password
        }
    )

    assert signup_response.status_code == 201

    saved_user = container.user_service.get_by_login(login)
    assert saved_user is not None

    response = client.post(
        "/auth/login",
        json={
            "login": login,
            "password": password
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["type"] == "Bearer"
    assert isinstance(data["accessToken"], str)
    assert isinstance(data["refreshToken"], str)

    assert data["accessToken"] != ""
    assert data["refreshToken"] != ""

    with app.app_context():
        user_id = container.jwt_provider.get_user_id(
            data["accessToken"]
        )

    assert user_id == saved_user.id


def test_login_invalid_credentials():
    client = app.test_client()

    login = f"test_{uuid4().hex}"
    password = "correct_password"

    signup_response = client.post(
        "/auth/signup",
        json={
            "login": login,
            "password": password
        }
    )

    assert signup_response.status_code == 201

    # Неправильный пароль
    response = client.post(
        "/auth/login",
        json={
            "login": login,
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401

    # Несуществующий пользователь
    response = client.post(
        "/auth/login",
        json={
            "login": "unknown_user",
            "password": password
        }
    )

    assert response.status_code == 401


def test_login_invalid_body():
    client = app.test_client()

    invalid_bodies = [
        {},
        {"login": "user"},
        {"password": "password"},
        {"login": 123, "password": "password"},
        {"login": "user", "password": 123},
    ]

    for body in invalid_bodies:
        response = client.post(
            "/auth/login",
            json=body
        )

        assert response.status_code == 400