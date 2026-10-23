from abc import ABC, abstractmethod
from uuid import UUID


from domain.model.game import Game as DomainGame
from domain.model.leaderboard import Leaderboard

class GameRepository(ABC):

    @abstractmethod
    def save(self, game: DomainGame) -> None:
        pass

    @abstractmethod
    def get(self, game_id: UUID) -> DomainGame | None:
        pass

    @abstractmethod
    def get_available_games(self) -> list[DomainGame]:
        pass

    @abstractmethod
    def get_completed_games_by_user(self, user_id: UUID) -> list[DomainGame]:
        pass

    @abstractmethod
    def get_leaderboard(self, limit: int) -> list[Leaderboard]:
        pass

