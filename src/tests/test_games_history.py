from datetime import datetime, timezone, timedelta
from uuid import uuid4

from app import app, container
from domain.model.board import Board
from domain.model.game import Game
from domain.model.game_status import GameStatus



def test_games_history():

    client = app.test_client()

    login = f"test_{uuid4().hex}"
    password = "correct_password"

    signup_response = client.post(
        "/auth/signup",
        json={
            "login": login,
            "password": password
        }
    )

    assert signup_response.status_code == 201

    saved_user = container.user_service.get_by_login(login)
    assert saved_user is not None
    user_id = saved_user.id


    # Авторизация
    response = client.post(
        "/auth/login",
        json={
            "login": login,
            "password": password
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    headers = {
        "Authorization": f"Bearer {data['accessToken']}"
    }

    now = datetime.now(timezone.utc)

    # Завершённая игра пользователя — должна попасть
    finished_game = Game(
        id=uuid4(),
        board=Board(cells=[
            [1, 1, 1],
            [2, 2, 0],
            [0, 0, 0]
        ]),
        player_1_id=user_id,
        player_2_id=uuid4(),
        game_status=GameStatus.FINISHED,
        current_turn_id=None,
        winner_id=user_id,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=False,
        created_at=now
    )

    # Ничья пользователя — тоже должна попасть
    draw_game = Game(
        id=uuid4(),
        board=Board(cells=[
            [1, 2, 1],
            [1, 2, 2],
            [2, 1, 1]
        ]),
        player_1_id=user_id,
        player_2_id=uuid4(),
        game_status=GameStatus.DRAW,
        current_turn_id=None,
        winner_id=None,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=False,
        created_at=now - timedelta(minutes=1)
    )

    # Незавершённая игра пользователя — не должна попасть
    in_progress_game = Game(
        id=uuid4(),
        board=Board(cells=[
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 0]
        ]),
        player_1_id=user_id,
        player_2_id=uuid4(),
        game_status=GameStatus.IN_PROGRESS,
        current_turn_id=user_id,
        winner_id=None,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=False,
        created_at=now - timedelta(minutes=2)
    )

    # Завершённая игра другого пользователя — не должна попасть
    other_game = Game(
        id=uuid4(),
        board=Board(cells=[
            [1, 1, 1],
            [2, 2, 0],
            [0, 0, 0]
        ]),
        player_1_id=uuid4(),
        player_2_id=uuid4(),
        game_status=GameStatus.FINISHED,
        current_turn_id=None,
        winner_id=None,
        player_1_symbol=1,
        player_2_symbol=2,
        is_computer_game=False,
        created_at=now - timedelta(minutes=3)
    )


    container.repository.save(finished_game)
    container.repository.save(draw_game)
    container.repository.save(in_progress_game)
    container.repository.save(other_game)

    # Тестируемый запрос
    response = client.get(
        "/games/history",
        headers=headers
    )

    assert response.status_code == 200

    history = response.get_json()

    assert len(history) == 2

    returned_ids = [game["id"] for game in history]

    assert str(finished_game.id) in returned_ids
    assert str(draw_game.id) in returned_ids

    assert str(in_progress_game.id) not in returned_ids
    assert str(other_game.id) not in returned_ids

    assert history[0]["id"] == str(finished_game.id)
    assert history[1]["id"] == str(draw_game.id)


    