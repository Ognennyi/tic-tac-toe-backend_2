from dataclasses import dataclass
from uuid import UUID

from domain.model.board import Board
from domain.model.game_status import GameStatus

from datetime import datetime

@dataclass
class Game:
    id: UUID
    board: Board
    player_1_id: UUID
    player_2_id: UUID | None
    game_status: GameStatus
    current_turn_id: UUID | None #Тот кто должен сходить
    winner_id: UUID | None
    player_1_symbol: int
    player_2_symbol: int
    is_computer_game: bool      # True - с компьютером.   False - с другим игроком
    created_at: datetime
    