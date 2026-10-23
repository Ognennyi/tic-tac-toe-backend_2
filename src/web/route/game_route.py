from flask import Blueprint, request, g
from uuid import UUID

from domain.service.game_service import GameService
from domain.service.user_service import UserService
from domain.model.board import Board as DomainBoard

def create_game_blueprint(game_service: GameService, user_service: UserService) -> Blueprint:
    game_blueprint = Blueprint('game', __name__)

    @game_blueprint.post("/game/<game_id>")
    def make_move(game_id):

        uuid_game_id = UUID(game_id)

        data = request.get_json()  # словарь

        domain_board = DomainBoard(data["board"])

        try:
            result_game = game_service.update_game(uuid_game_id, g.user_id, domain_board)
        except ValueError as error:
            return{
                "error": str(error)
            }, 400


        return {
            "id": str(result_game.id),
            "board": result_game.board.cells,
            "game_status": result_game.game_status.value,
            "current_turn_id": str(result_game.current_turn_id) if result_game.current_turn_id is not None else None,
            "winner_id": str(result_game.winner_id) if result_game.winner_id is not None else None 
        }
    

    @game_blueprint.post("/game")
    def create_game():

        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            return{
                "error": "Error with is_computer_game"
            }, 400
        
        if "is_computer_game" in data and isinstance(data["is_computer_game"], bool):

            new_game = game_service.create_game(g.user_id, data["is_computer_game"])

            return{
                    "id": str(new_game.id),
                    "game_status": str(new_game.game_status.value)
                    },201
        else:
            return{
                "error": "Error with is_computer_game"
            }, 400
        


    @game_blueprint.get("/games/available")
    def get_available_games():

        games_list = game_service.get_available_games()  # список объектов Game

        result_list = []

        for game in games_list:
            slovar = dict()
            slovar["id"] = str(game.id)
            slovar["player_1_id"] = str(game.player_1_id)
            slovar["game_status"] = game.game_status.value
            result_list.append(slovar)

        return result_list, 200


    @game_blueprint.post("/games/<game_id>/join")
    def join_game(game_id):

        try:
            uuid_game_id = UUID(game_id)
            game = game_service.join_game(uuid_game_id, g.user_id)
        except ValueError:
            return{
                "message": "Невозможно подключиться к игре"
            },400


        return{
                "id": str(game.id),
                "player_1_id": str(game.player_1_id),
                "player_2_id": str(game.player_2_id),
                "game_status": game.game_status.value
            }




    @game_blueprint.get("/game/<game_id>")
    def get_game(game_id):

        try:
            game = game_service.get_game(game_id)
            return{
                "id": str(game_id),
                "board": game.board.cells,
                "player_1_id": str(game.player_1_id),
                "player_2_id": str(game.player_2_id) if game.player_2_id is not None else None,
                "game_status": game.game_status.value,
                "current_turn_id": str(game.current_turn_id) if game.current_turn_id is not None else None,
                "winner_id": str(game.winner_id) if game.winner_id is not None else None ,
                "player_1_symbol": game.player_1_symbol,
                "player_2_symbol": game.player_2_symbol,
                "is_computer_game": game.is_computer_game
            }
        except ValueError:
            return{
                "message": "Игра не найдена"
            },404
        


    @game_blueprint.get("/games/history")
    def get_history_games():

        games_list = game_service.get_completed_games_by_user(g.user_id)  # список объектов Game

        result_list = []

        for game in games_list:
            slovar = dict()
            slovar["id"] = str(game.id)
            slovar["game_status"] = game.game_status.value
            slovar["winner_id"] = str(game.winner_id) if game.winner_id is not None else None
            slovar["created_at"] = game.created_at.isoformat()
            result_list.append(slovar)

        return result_list, 200
    

    @game_blueprint.get("/games/leaderboard")

    def get_leaderboard_games():

        number = request.args.get("number", type=int)

        if number is None or number <= 0:
            return{
                "message": "Некорректное N"
            },400

        result_list = game_service.get_leaderboard(number)

        result = []

        for row in result_list:
            user = user_service.get(row.user_id)

            if user is None:
                continue

            result.append({
                "user_id": str(row.user_id),
                "login": user.login,
                "win_ratio": row.win_ratio
            })


        return result, 200

        


    return game_blueprint




