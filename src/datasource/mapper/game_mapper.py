from domain.model.board import Board as  DomainBoard
from domain.model.game import Game as DomainGame
from datasource.model.game import Game as DatasourceGame

from domain.model.game_status import GameStatus


# 1. domain.Game -> datasource.Game
# 2. datasource.Game -> domain.Game

def to_datasource(game: DomainGame) -> DatasourceGame:    #Из домена в датасорс - 1 случай

    game_id = game.id
    return DatasourceGame(
        id=game_id, 
        board = game.board.cells,

        player_1_id = game.player_1_id,
        player_2_id = game.player_2_id,
        game_status = game.game_status.value,
        current_turn_id= game.current_turn_id,
        winner_id = game.winner_id,
        player_1_symbol =  game.player_1_symbol,
        player_2_symbol = game.player_2_symbol,
        is_computer_game = game.is_computer_game,
        created_at = game.created_at
        )



def to_domain(game: DatasourceGame) -> DomainGame:
    game_id = game.id
    domain_board = DomainBoard(game.board)

    return DomainGame(
        id = game_id,
        board = domain_board,
        player_1_id = game.player_1_id,
        player_2_id = game.player_2_id,
        game_status = GameStatus(game.game_status),
        current_turn_id= game.current_turn_id,
        winner_id = game.winner_id,
        player_1_symbol =  game.player_1_symbol,
        player_2_symbol = game.player_2_symbol,
        is_computer_game = game.is_computer_game,
        created_at = game.created_at
        )