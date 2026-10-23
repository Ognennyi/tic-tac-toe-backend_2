from uuid import uuid4

from werkzeug.security import check_password_hash

from di.container import Container
from domain.model.sign_up_request import SignUpRequest



def test_sign_up():
    container = Container()
    auth_service = container.auth_service

    login = f"test_{uuid4().hex}"
    password = "test_password_123"

    request = SignUpRequest(
        login=login,
        password=password
    )

    # Первая регистрация должна пройти успешно
    result = auth_service.sign_up(request)

    assert result is True

    # Проверяем, что пользователь появился в PostgreSQL
    saved_user = container.user_service.get_by_login(login)

    assert saved_user is not None
    assert saved_user.login == login

    # Проверяем, что пароль хранится в виде хеша
    assert saved_user.password != password
    assert check_password_hash(saved_user.password, password)

    # Повторная регистрация с тем же логином запрещена
    second_result = auth_service.sign_up(request)

    assert second_result is False