
from uuid import uuid4
from app import app

from di.container import Container
from domain.model.sign_up_request import SignUpRequest

from domain.model.JwtRequest import JwtRequest



def test_authenticate():
    container = Container()
    auth_service = container.auth_service

    login = f"test_{uuid4().hex}"
    password = "correct_password"

    # Регистрируем пользователя
    sign_up_request = SignUpRequest(
        login=login,
        password=password
    )

    assert auth_service.sign_up(sign_up_request) is True

    saved_user = container.user_service.get_by_login(login)

    assert saved_user is not None

    # Правильные логин и пароль
    jwt_request = JwtRequest(
        login=login,
        password=password
    )

    with app.app_context():
        response = auth_service.authenticate(jwt_request)

        assert response is not None
        assert response.type == "Bearer"
        assert response.access_token != ""
        assert response.refresh_token != ""

        user_id = container.jwt_provider.get_user_id(
            response.access_token
        )

        assert user_id == saved_user.id

    # Неправильный пароль
    wrong_password_request = JwtRequest(
        login=login,
        password="wrong_password"
    )

    with app.app_context():
        assert auth_service.authenticate(wrong_password_request) is None

    # Несуществующий пользователь
    unknown_user_request = JwtRequest(
        login=f"unknown_{uuid4().hex}",
        password=password
    )

    with app.app_context():
        assert auth_service.authenticate(unknown_user_request) is None