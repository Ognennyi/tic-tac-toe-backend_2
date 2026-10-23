from uuid import uuid4

import pytest

from di.container import Container
from domain.model.game_status import GameStatus


@pytest.mark.parametrize(
    "is_computer_game, expected_status",
    [
        (True, GameStatus.IN_PROGRESS),
        (False, GameStatus.WAITING),
    ]
)
def test_create_game(is_computer_game, expected_status):
    container = Container()

    user_id = uuid4()

    # Создаём игру через сервис
    game = container.service.create_game(
        user_id=user_id,
        is_computer_game=is_computer_game
    )

    # Проверяем созданную игру
    assert game.id is not None
    assert game.player_1_id == user_id
    assert game.player_2_id is None
    assert game.game_status == expected_status
    assert game.is_computer_game == is_computer_game

    assert game.player_1_symbol == 1
    assert game.player_2_symbol == 2
    assert game.winner_id is None

    assert game.board.cells == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    if is_computer_game:
        assert game.current_turn_id == user_id
    else:
        assert game.current_turn_id is None

    # Проверяем сохранение в PostgreSQL
    saved_game = container.repository.get(game.id)

    assert saved_game is not None
    assert saved_game.id == game.id
    assert saved_game.game_status == expected_status
    assert saved_game.player_1_id == user_id
    assert saved_game.is_computer_game == is_computer_game