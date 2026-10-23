from uuid import uuid4

from werkzeug.security import check_password_hash

from app import app, container


def test_signup_success():
    client = app.test_client()

    login = f"test_{uuid4().hex}"
    password = "test_password"

    response = client.post(
        "/auth/signup",
        json={
            "login": login,
            "password": password
        }
    )

    assert response.status_code == 201

    saved_user = container.user_service.get_by_login(login)

    assert saved_user is not None
    assert saved_user.login == login
    assert saved_user.password != password
    assert check_password_hash(saved_user.password, password)


def test_signup_duplicate_login():
    client = app.test_client()

    login = f"test_{uuid4().hex}"

    data = {
        "login": login,
        "password": "test_password"
    }

    first_response = client.post("/auth/signup", json=data)
    second_response = client.post("/auth/signup", json=data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_signup_invalid_data():
    client = app.test_client()

    invalid_requests = [
        {"login": "test"},
        {"password": "123456"},
        {"login": 123, "password": "123456"},
        {"login": "test", "password": None},
        ["test", "123456"]
    ]

    for data in invalid_requests:
        response = client.post("/auth/signup", json=data)

        assert response.status_code == 400


def test_signup_invalid_json():
    client = app.test_client()

    response = client.post(
        "/auth/signup",
        data='{"login":',
        content_type="application/json"
    )

    assert response.status_code == 400