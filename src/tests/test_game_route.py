from uuid import uuid4

from app import app



def register_user(client, login, password):
    return client.post(
        "/auth/signup",
        json={
            "login": login,
            "password": password
        }
    )



def create_auth_header(client, login, password):
    response = client.post(
        "/auth/login",
        json={
            "login": login,
            "password": password
        }
    )

    assert response.status_code == 200

    access_token = response.get_json()["accessToken"]

    return {
        "Authorization": f"Bearer {access_token}"
    }



def test_game_route():
    client = app.test_client()

    login = f"user_{uuid4().hex}"
    password = "123456"

    register_user(client, login, password)

    headers = create_auth_header(client, login, password)

    # Создаём игру с компьютером
    response = client.post(
        "/game",
        json={
            "is_computer_game": True
        },
        headers=headers
    )

    assert response.status_code == 201

    game_id = response.get_json()["id"]

    # Пользователь делает ход
    response = client.post(
        f"/game/{game_id}",
        json={
            "board": [
                [1, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == game_id
    assert data["board"][0][0] == 1
    assert data["game_status"] == "in_progress"

    # Проверяем, что компьютер тоже сделал один ход
    computer_symbols = 0

    for row in data["board"]:
        computer_symbols += row.count(2)

    assert computer_symbols == 1


def test_game_route_invalid_move():
    client = app.test_client()

    login = f"user_{uuid4().hex}"
    password = "123456"

    register_user(client, login, password)

    headers = create_auth_header(client, login, password)

    response = client.post(
        "/game",
        json={
            "is_computer_game": True
        },
        headers=headers
    )

    game_id = response.get_json()["id"]

    # Игрок пытается поставить сразу две единицы
    response = client.post(
        f"/game/{game_id}",
        json={
            "board": [
                [1, 1, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
        },
        headers=headers
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "error": "Некорректный ввод"
    }


def test_available_games_and_join():
    client = app.test_client()

    login_1 = f"user_{uuid4().hex}"
    login_2 = f"user_{uuid4().hex}"

    password = "123456"

    register_user(client, login_1, password)
    register_user(client, login_2, password)

    headers_1 = create_auth_header(client, login_1, password)
    headers_2 = create_auth_header(client, login_2, password)

    # Первый пользователь создаёт игру
    response = client.post(
        "/game",
        json={
            "is_computer_game": False
        },
        headers=headers_1
    )

    assert response.status_code == 201

    game_id = response.get_json()["id"]

    # Второй пользователь получает список доступных игр
    response = client.get(
        "/games/available",
        headers=headers_2
    )

    assert response.status_code == 200

    games = response.get_json()

    game_found = False

    for game in games:
        if game["id"] == game_id:
            game_found = True

    assert game_found is True

    # Второй пользователь подключается
    response = client.post(
        f"/games/{game_id}/join",
        headers=headers_2
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == game_id
    assert data["game_status"] == "in_progress"
    assert data["player_2_id"] is not None


def test_get_game():
    client = app.test_client()

    login = f"user_{uuid4().hex}"
    password = "123456"

    register_user(client, login, password)

    headers = create_auth_header(client, login, password)

    response = client.post(
        "/game",
        json={
            "is_computer_game": True
        },
        headers=headers
    )

    game_id = response.get_json()["id"]

    response = client.get(
        f"/game/{game_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == game_id
    assert data["board"] == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert data["game_status"] == "in_progress"
    assert data["player_1_symbol"] == 1
    assert data["player_2_symbol"] == 2
    assert data["is_computer_game"] is True


def test_game_route_without_auth():
    client = app.test_client()

    response = client.post(
        "/game",
        json={
            "is_computer_game": True
        }
    )

    assert response.status_code == 401