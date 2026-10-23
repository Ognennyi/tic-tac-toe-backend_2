
from web.model.game import WebGame
from web.model.board import WebBoard

from domain.model.game import Game as DomainGame
from domain.model.board import Board as DomainBoard



def to_domain(web_game: WebGame)-> DomainGame:
    domain_id = web_game.id
    domain_board = DomainBoard(web_game.board.cells)
    return DomainGame(domain_id, domain_board)


def to_web(domain_game: DomainGame)-> WebGame:
    web_id = domain_game.id
    web_board = WebBoard(domain_game.board.cells)
    return WebGame(web_id, web_board)