from abc import ABC, abstractmethod
from uuid import UUID
from domain.model.user import User as DomainUser


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: DomainUser) -> None:
        pass

    @abstractmethod
    def get(self, user_id: UUID) -> DomainUser | None:
        pass

    @abstractmethod
    def get_by_login(self, user_login: str) -> DomainUser | None:
        pass
