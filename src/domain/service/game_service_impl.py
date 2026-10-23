from datasource.repository.game_repository import GameRepository
from domain.model.game import Game
from domain.service.game_service import GameService

from domain.model.board import Board

from domain.model.leaderboard import Leaderboard

from uuid import UUID, uuid4
from domain.model.game_status import GameStatus

from datetime import datetime, timezone

import copy




class GameServiceImpl(GameService): 

    def __init__(self, repository: GameRepository):
        self.repository = repository


    def make_computer_move(self, game: Game) -> Game:  


        best_score = -1000
        best_move = None

        board = game.board.cells  # списки в списке

        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2

                    score = self.minimax(board, False)

                    board[i][j] = 0

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move is not None:
            board[best_move[0]][best_move[1]] = 2

        if self.is_game_over(game):         #игра закончена после хода компьютера
            game.current_turn_id = None
            who_winner = self.get_winner(board)
            if who_winner == 0:
                game.game_status = GameStatus.DRAW
                game.winner_id = None
                
            elif who_winner == 2:
                game.game_status = GameStatus.FINISHED
                game.winner_id = None

        else:    #игра не закончена после хода компьютера 
            game.game_status = GameStatus.IN_PROGRESS
            game.current_turn_id = game.player_1_id

        return game


    def minimax(
            self,
            board: list[list[int]],
            is_maximizing: bool,
            depth: int = 0
    ) -> int:

        winner = self.get_winner(board)

        if winner == 2:
            return 10 - depth

        if winner == 1:
            return depth - 10

        # Проверка на ничью
        board_is_full = True

        for row in board:
            if 0 in row:
                board_is_full = False
                break

        if board_is_full:
            return 0

        # Ход компьютера
        if is_maximizing:
            best_score = -1000

            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 2

                        score = self.minimax(
                            board,
                            False,
                            depth + 1
                        )

                        board[i][j] = 0

                        if score > best_score:
                            best_score = score

            return best_score

        # Ход пользователя
        else:
            best_score = 1000

            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1

                        score = self.minimax(
                            board,
                            True,
                            depth + 1
                        )

                        board[i][j] = 0

                        if score < best_score:
                            best_score = score

            return best_score







    def validate_game(self, old_game: Game, new_game: Game, player_symbol: int) -> bool: #*ход игрока проверяем
        if old_game.id != new_game.id: # Проверка   UUID
            return False

        if len(new_game.board.cells) == 3:    #Проверка размеров матрицы
            for cell in new_game.board.cells:
                if len(cell) != 3:
                    return False
        else:
            return False

        old_board = old_game.board.cells
        new_board = new_game.board.cells
        changes = 0

        for i in range(3):       # Проверка на изменение числа 1 или 2 на 0
            for j in range(3):
                old_cell = old_board[i][j]
                new_cell = new_board[i][j]
                if old_cell == new_cell:
                    continue

                if old_cell == 0 and new_cell == player_symbol:
                    changes += 1
                else:
                    return False

        if changes == 1:
            return True
        else:
            return False


    def is_game_over(self, game: Game) -> bool:
        board = game.board.cells

        for line in range(3):
            if (board[line][0] == board[line][1] == board[line][2]) and (board[line][0] != 0):
                    return True

            if (board[0][line] == board[1][line] == board[2][line]) and (board[0][line] != 0):
                    return True

        if ( (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]) ) and (board[1][1] != 0):
            return True

        if 0 not in board[0] and 0 not in board[1] and 0 not in board[2]:
            return True

        return False


    def get_winner(self, board: list[list[int]]) -> int:

        for line in range(3):
            if (board[line][0] == board[line][1] == board[line][2]) and (board[line][0] != 0):
                return board[line][0]

            if (board[0][line] == board[1][line] == board[2][line]) and (board[0][line] != 0):
                return board[0][line]

        if ((board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0])) and ( board[1][1] != 0):
            return board[1][1]

        return 0

    
    def create_game(self, user_id: UUID, is_computer_game: bool) -> Game:
        
        new_game_uuid = uuid4()

        new_game_board=Board(cells=[
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ])
        if is_computer_game:
            new_game_status = GameStatus.IN_PROGRESS
            new_current_turn_id = user_id

        else:
            new_game_status = GameStatus.WAITING
            new_current_turn_id = None

        

        new_game = Game(
            id = new_game_uuid,
            board = new_game_board,
            player_1_id = user_id,
            player_2_id = None,
            game_status =  new_game_status,
            current_turn_id = new_current_turn_id,    #Тот кто должен сходить
            winner_id = None,
            player_1_symbol = 1,
            player_2_symbol = 2,
            is_computer_game = is_computer_game,
            created_at = datetime.now(timezone.utc)
        )

        self.repository.save(new_game)

        return new_game
    

    
    def get_available_games(self) -> list[Game]:
        return self.repository.get_available_games()



    def join_game(self, game_id: UUID, user_id: UUID) -> Game:
        # game_id - UUID игры, к которой хотим присоединиться.
        # user_id - UUID авторизованного пользователя.

        game = self.repository.get(game_id)

        if game is None:
            raise ValueError("Игра не найдена")
        
        if game.game_status == GameStatus.WAITING and game.is_computer_game == False and game.player_2_id is None and game.player_1_id != user_id:
            game.player_2_id = user_id
            game.game_status = GameStatus.IN_PROGRESS
            game.current_turn_id = game.player_1_id
            self.repository.save(game)
            return game
        else:
            raise ValueError("Невозможно подключиться к игре")



    def update_game(self, game_id: UUID, user_id: UUID, board: Board) -> Game:

        game = self.repository.get(game_id)

        if game is None:
            raise ValueError("Игра не найдена")
        
        if game.game_status != GameStatus.IN_PROGRESS:
            raise ValueError("Статус игры не позволяет сделать ход")


        if game.player_1_id != user_id and game.player_2_id != user_id:
            raise ValueError("Нет доступа к данной игре")
        

        if user_id != game.current_turn_id:
            raise ValueError("Ход должен сделать другой пользователь")
        
        
        # Начинается выполнение хода который получила функция

        new_game = copy.deepcopy(game)
        new_game.board = board
        
        if user_id == game.player_1_id:
            symbol = game.player_1_symbol
        else:
            symbol = game.player_2_symbol
        

        if not self.validate_game(game , new_game, symbol):
            raise ValueError("Некорректный ввод")
        
        
        if self.is_game_over(new_game):

            player_who_win = self.get_winner(new_game.board.cells)
            new_game.current_turn_id = None

            if player_who_win == 1:
                new_game.winner_id = new_game.player_1_id
                new_game.game_status = GameStatus.FINISHED

            elif player_who_win == 2:
                new_game.winner_id = new_game.player_2_id
                new_game.game_status = GameStatus.FINISHED

            else:
                new_game.game_status = GameStatus.DRAW
                new_game.winner_id = None

        else:  #Если игра не закончилась
            if new_game.is_computer_game:
                new_game = self.make_computer_move(new_game)
                
            else: #Если следующий ход человека
                if user_id == new_game.player_1_id:
                    new_game.current_turn_id = new_game.player_2_id
                else:
                    new_game.current_turn_id = new_game.player_1_id

        

        self.repository.save(new_game)
        return new_game



    def get_game(self, game_id: UUID) -> Game:
        game_id = UUID(game_id)
        game = self.repository.get(game_id)
        if game is None:
            raise ValueError("Игра не найдена")
        
        return game
    
    def get_completed_games_by_user(self, user_id: UUID) -> list[Game]:
        return self.repository.get_completed_games_by_user(user_id)
    

    def get_leaderboard(self, limit: int) -> list[Leaderboard]:
        return self.repository.get_leaderboard(limit)



            

        


        


        



