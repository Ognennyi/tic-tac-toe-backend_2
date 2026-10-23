from uuid import uuid4

from di.container import Container
from domain.model.board import Board
from domain.model.game import Game
from domain.model.game_status import GameStatus

from datetime import datetime, timezone

def test_save_and_get_new_game():
    container = Container()
    repository = container.repository

    game_id = uuid4()
    player_id = uuid4()

    game = Game(
        id=game_id,
        board=Board([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        player_1_id=player_id,
        player_2_id=None,
        game_status=GameStatus.WAITING,
        current_turn_id=None,
        winner_id=None,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=False,
        created_at=datetime.now(timezone.utc)
    )

    # Сохраняем игру
    repository.save(game)

    # Получаем её обратно из PostgreSQL
    saved_game = repository.get(game_id)

    assert saved_game is not None

    assert saved_game.id == game.id
    assert saved_game.board.cells == game.board.cells

    assert saved_game.player_1_id == player_id
    assert saved_game.player_2_id is None

    assert saved_game.game_status == GameStatus.WAITING
    assert saved_game.current_turn_id is None
    assert saved_game.winner_id is None

    assert saved_game.player_1_symbol == 1
    assert saved_game.player_2_symbol == 2
    assert saved_game.is_computer_game is False