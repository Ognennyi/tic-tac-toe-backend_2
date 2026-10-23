from uuid import uuid4

from domain.model.board import Board as DomainBoard
from domain.model.game import Game as DomainGame
from datasource.model.game import Game as DatasourceGame
from datasource.mapper.game_mapper import to_datasource, to_domain
from domain.model.game_status import GameStatus

from datetime import datetime, timezone


def test_game_mapper():
    game_id = uuid4()
    
    player_1_id = uuid4()
    player_2_id = uuid4()

    cells = [
        [1, 0, 0],
        [0, 2, 0],
        [0, 0, 0]
    ]

    # Создаём доменную модель
    domain_game = DomainGame(
        id=game_id,
        board=DomainBoard(cells),
        player_1_id = player_1_id,
        player_2_id = player_2_id,
        game_status =  GameStatus.IN_PROGRESS,
        current_turn_id = player_1_id, 
        winner_id = None,
        player_1_symbol = 1,
        player_2_symbol = 2,
        is_computer_game = False,
        created_at=datetime.now(timezone.utc)

    )

    # Domain -> Datasource
    datasource_game = to_datasource(domain_game)

    assert isinstance(datasource_game, DatasourceGame)
    assert datasource_game.id == game_id
    assert datasource_game.board == cells
    assert datasource_game.player_1_id == player_1_id
    assert datasource_game.player_2_id == player_2_id
    assert datasource_game.game_status == GameStatus.IN_PROGRESS.value
    assert datasource_game.current_turn_id == player_1_id
    assert datasource_game.winner_id is None
    assert datasource_game.player_1_symbol == 1
    assert datasource_game.player_2_symbol == 2
    assert datasource_game.is_computer_game is False

    # Datasource -> Domain
    new_domain_game = to_domain(datasource_game)

    assert isinstance(new_domain_game, DomainGame)
    assert new_domain_game.id == game_id
    assert new_domain_game.board.cells == cells
    assert new_domain_game.player_1_id == player_1_id
    assert new_domain_game.player_2_id == player_2_id
    assert new_domain_game.game_status == GameStatus.IN_PROGRESS
    assert new_domain_game.current_turn_id == player_1_id
    assert new_domain_game.winner_id is None
    assert new_domain_game.player_1_symbol == 1
    assert new_domain_game.player_2_symbol == 2
    assert new_domain_game.is_computer_game is False
