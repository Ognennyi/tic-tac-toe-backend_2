from uuid import uuid4

from domain.model.user import User as DomainUser
from datasource.database import SessionLocal
from datasource.repository.user_repository_impl import UserRepositoryImpl


def test_user_repository_save_and_get():
    repository = UserRepositoryImpl(SessionLocal)

    user_id = uuid4()
    login = f"user_{user_id.hex}"

    user = DomainUser(
        id=user_id,
        login=login,
        password="test_hash"
    )

    # 1. Сохраняем пользователя в PostgreSQL
    repository.save(user)

    # 2. Ищем пользователя по UUID
    saved_user = repository.get(user_id)

    assert saved_user is not None
    assert saved_user.id == user.id
    assert saved_user.login == user.login
    assert saved_user.password == user.password

    # 3. Ищем пользователя по логину
    found_user = repository.get_by_login(login)

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.login == user.login
    assert found_user.password == user.password

    # 4. Проверяем поиск несуществующего пользователя
    missing_user = repository.get_by_login("nonexistent_" + uuid4().hex)

    assert missing_user is None