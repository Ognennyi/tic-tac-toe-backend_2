from abc import ABC, abstractmethod
from domain.model.game import Game
from uuid import UUID
from domain.model.game import Game as DomainGame
from domain.model.board import Board

from domain.model.leaderboard import Leaderboard

class GameService(ABC):

    @abstractmethod
    def make_computer_move(self, game: Game) -> Game:
        pass

    @abstractmethod
    def validate_game(self, old_game: Game, new_game: Game, symbol: int) -> bool:
        pass

    @abstractmethod
    def is_game_over(self, game: Game) -> bool:
        pass

    @abstractmethod
    def create_game(self, user_id: UUID, is_computer_game: bool) -> Game:
        pass


    @abstractmethod
    def get_available_games(self) -> list[DomainGame]:
        pass

    @abstractmethod
    def join_game(self, game_id: UUID, user_id: UUID) -> Game:
        pass

    @abstractmethod
    def update_game(self, game_id: UUID, user_id: UUID, board: Board) -> Game:
        pass

    @abstractmethod
    def get_game(self, game_id: UUID) -> Game:
        pass
    
    @abstractmethod
    def get_completed_games_by_user(self, user_id: UUID) -> list[Game]:
        pass

    @abstractmethod
    def get_leaderboard(self, limit: int) -> list[Leaderboard]:
        pass
    