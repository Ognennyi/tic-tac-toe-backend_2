import pytest

from uuid import uuid4

from domain.model.game import Game
from domain.model.board import Board
from domain.model.game_status import GameStatus
from domain.service.game_service_impl import GameServiceImpl

from datasource.repository.game_repository_impl import GameRepositoryImpl
from datasource.database import SessionLocal

from datetime import datetime, timezone

def test_invalid_move():
    repository = GameRepositoryImpl(SessionLocal)
    service = GameServiceImpl(repository)

    game_id = uuid4()
    player_id = uuid4()

    game = Game(
        id=game_id,
        board=Board([
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 0]
        ]),
        player_1_id=player_id,
        player_2_id=None,
        game_status=GameStatus.IN_PROGRESS,
        current_turn_id=player_id,
        winner_id=None,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=True,
        created_at=datetime.now(timezone.utc)
    )

    repository.save(game)

    new_board = Board([
        [0, 1, 0],
        [0, 2, 0],
        [0, 0, 0]
    ])

    with pytest.raises(ValueError):
        service.update_game(game_id, player_id, new_board)

    saved_game = repository.get(game_id)

    assert saved_game is not None
    assert saved_game.board.cells == game.board.cells


def test_human_win():
    repository = GameRepositoryImpl(SessionLocal)
    service = GameServiceImpl(repository)

    game_id = uuid4()
    player_id = uuid4()

    game = Game(
        id=game_id,
        board=Board([
            [1, 1, 0],
            [2, 2, 0],
            [0, 0, 0]
        ]),
        player_1_id=player_id,
        player_2_id=None,
        game_status=GameStatus.IN_PROGRESS,
        current_turn_id=player_id,
        winner_id=None,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=True,
        created_at=datetime.now(timezone.utc)
    )

    repository.save(game)

    new_board = Board([
        [1, 1, 1],
        [2, 2, 0],
        [0, 0, 0]
    ])

    result = service.update_game(game_id, player_id, new_board)

    assert result.board.cells == [
        [1, 1, 1],
        [2, 2, 0],
        [0, 0, 0]
    ]

    assert result.game_status == GameStatus.FINISHED
    assert result.winner_id == player_id
    assert result.current_turn_id is None


def test_draw_game():
    repository = GameRepositoryImpl(SessionLocal)
    service = GameServiceImpl(repository)

    game_id = uuid4()
    player_id = uuid4()

    game = Game(
        id=game_id,
        board=Board([
            [1, 1, 2],
            [2, 2, 1],
            [1, 2, 0]
        ]),
        player_1_id=player_id,
        player_2_id=None,
        game_status=GameStatus.IN_PROGRESS,
        current_turn_id=player_id,
        winner_id=None,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=True,
        created_at=datetime.now(timezone.utc)
    )

    repository.save(game)

    new_board = Board([
        [1, 1, 2],
        [2, 2, 1],
        [1, 2, 1]
    ])

    result = service.update_game(game_id, player_id, new_board)

    assert result.board.cells == [
        [1, 1, 2],
        [2, 2, 1],
        [1, 2, 1]
    ]

    assert result.game_status == GameStatus.DRAW
    assert result.winner_id is None
    assert result.current_turn_id is None


def test_computer_win():
    repository = GameRepositoryImpl(SessionLocal)
    service = GameServiceImpl(repository)

    game_id = uuid4()
    player_id = uuid4()

    game = Game(
        id=game_id,
        board=Board([
            [2, 2, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]),
        player_1_id=player_id,
        player_2_id=None,
        game_status=GameStatus.IN_PROGRESS,
        current_turn_id=player_id,
        winner_id=None,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=True,
        created_at=datetime.now(timezone.utc)
    )

    repository.save(game)

    new_board = Board([
        [2, 2, 0],
        [1, 1, 0],
        [0, 0, 1]
    ])

    result = service.update_game(game_id, player_id, new_board)

    assert result.board.cells == [
        [2, 2, 2],
        [1, 1, 0],
        [0, 0, 1]
    ]

    assert result.game_status == GameStatus.FINISHED
    assert result.winner_id is None
    assert result.current_turn_id is None