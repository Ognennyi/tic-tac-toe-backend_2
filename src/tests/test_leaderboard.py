from datetime import datetime, timezone
from uuid import uuid4

from app import app, container
from domain.model.board import Board
from domain.model.game import Game
from domain.model.game_status import GameStatus


def test_leaderboard():
    client = app.test_client()

    # Создаю 3 пользователей
    password = "123456"

    login_1 = f"user_{uuid4().hex}"
    login_2 = f"user_{uuid4().hex}"
    login_3 = f"user_{uuid4().hex}"

    client.post(
        "/auth/signup",
        json={"login": login_1, "password": password}
    )

    client.post(
        "/auth/signup",
        json={"login": login_2, "password": password}
    )

    client.post(
        "/auth/signup",
        json={"login": login_3, "password": password}
    )

    user_1 = container.user_service.get_by_login(login_1)
    user_2 = container.user_service.get_by_login(login_2)
    user_3 = container.user_service.get_by_login(login_3)

    assert user_1 is not None
    assert user_2 is not None
    assert user_3 is not None

    # Создаю завершённые игры
    # user_1 дважды победил user_2
    # user_3 один раз победил user_1
    
    # В итоге:
    # user_1 -> 2 победы / 1 не победа = ratio 2
    # user_2 -> 0 побед / 2 не победы = ratio 0
    # user_3 -> 1 победа / 0 не побед = исключится

    games = [
        Game(
            id=uuid4(),
            board=Board(cells=[
                [1, 1, 1],
                [2, 2, 0],
                [0, 0, 0]
            ]),
            player_1_id=user_1.id,
            player_2_id=user_2.id,
            game_status=GameStatus.FINISHED,
            current_turn_id=None,
            winner_id=user_1.id,
            player_1_symbol=1,
            player_2_symbol=2,
            is_computer_game=False,
            created_at=datetime.now(timezone.utc)
        ),

        Game(
            id=uuid4(),
            board=Board(cells=[
                [1, 1, 1],
                [2, 2, 0],
                [0, 0, 0]
            ]),
            player_1_id=user_1.id,
            player_2_id=user_2.id,
            game_status=GameStatus.FINISHED,
            current_turn_id=None,
            winner_id=user_1.id,
            player_1_symbol=1,
            player_2_symbol=2,
            is_computer_game=False,
            created_at=datetime.now(timezone.utc)
        ),

        Game(
            id=uuid4(),
            board=Board(cells=[
                [1, 1, 0],
                [2, 2, 2],
                [1, 0, 0]
            ]),
            player_1_id=user_1.id,
            player_2_id=user_3.id,
            game_status=GameStatus.FINISHED,
            current_turn_id=None,
            winner_id=user_3.id,
            player_1_symbol=1,
            player_2_symbol=2,
            is_computer_game=False,
            created_at=datetime.now(timezone.utc)
        )
    ]

    for game in games:
        container.repository.save(game)

    # Авторизуемся и получаем Bearer header
    login_response = client.post(
        "/auth/login",
        json={
            "login": login_1,
            "password": password
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.get_json()["accessToken"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }


    response_leaderboard = client.get(
        "/games/leaderboard?number=2",
        headers = headers
    )

    assert response_leaderboard.status_code == 200

    data = response_leaderboard.get_json()

    for user_leader in data:
        assert "user_id" in user_leader
        assert "login" in user_leader
        assert "win_ratio" in user_leader

    
    user_1_data = next(
        user for user in data
        if user["login"] == login_1)

    user_2_data = next(
        user for user in data
        if user["login"] == login_2)

    # user_1 есть в результате
    assert user_1_data is not None

    # user_1 имеет ratio = 2 / 1 = 2.0
    assert user_1_data["win_ratio"] == 2.0

    # user_2 есть в результате
    assert user_2_data is not None

    # user_2 имеет ratio = 0 / 2 = 0.0
    assert user_2_data["win_ratio"] == 0.0

    # user_3 не должен попасть:
    # у него 1 победа и 0 поражений/ничьих
    returned_logins = [
        user["login"]
        for user in data
    ]

    assert login_3 not in returned_logins

