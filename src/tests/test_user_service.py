from uuid import uuid4

from di.container import Container
from domain.model.user import User


def test_user_service():
    container = Container()
    service = container.user_service

    user_id = uuid4()
    login = f"test_{user_id.hex}"

    user = User(
        id=user_id,
        login=login,
        password="test_hash"
    )

    # Создаём пользователя через сервис
    service.create_user(user)

    # Ищем его через сервис
    result = service.get_by_login(login)

    assert result is not None
    assert result.id == user_id
    assert result.login == login
    assert result.password == "test_hash"