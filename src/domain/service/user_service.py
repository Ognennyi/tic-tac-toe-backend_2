from uuid import UUID
from abc import ABC, abstractmethod
from domain.model.user import User


class UserService(ABC):

    @abstractmethod
    def create_user(self, user: User) -> None:
        pass


    @abstractmethod
    def get_by_login(self, login: str) -> User | None:
        pass


    @abstractmethod
    def get(self, user_id: UUID) -> User | None:
        pass


    