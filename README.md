# Tic-Tac-Toe REST API

Backend игры «Крестики-нолики», разработанный на Python и Flask.

## Возможности

- Регистрация пользователей и вход по логину и паролю.
- Авторизация через JWT (Access Token и Refresh Token).
- Игра против компьютера с алгоритмом Minimax.
- Игра между двумя пользователями.
- Просмотр истории завершённых игр и рейтинга игроков.
- Хранение пользователей и игр в PostgreSQL.

## Технологии

Python, Flask, Flask-JWT-Extended, SQLAlchemy, PostgreSQL, Psycopg, Pytest.

## Запуск

1. Установите Python и PostgreSQL.
2. Создайте базу данных `tic_tac_toe` с помощью PostgreSQL (например, командой `CREATE DATABASE tic_tac_toe;` в `psql`). Приложение подключается к `localhost:5432` под пользователем `postgres`.
3. Создайте виртуальное окружение и установите зависимости:

   ```bash
   python -m venv .venv
   pip install -r requirements.txt
   ```

   Перед установкой активируйте окружение: `.venv\Scripts\Activate.ps1` в PowerShell или `source .venv/bin/activate` в Linux/macOS.

4. Скопируйте `.env.example` в `.env` в корне проекта и задайте пароль от PostgreSQL и секретный ключ JWT.
5. Создайте таблицы в базе данных и запустите сервер:

   ```bash
   cd src
   python -c "from datasource.model.user import User; from datasource.model.game import Game; from datasource.database import Base, engine; Base.metadata.create_all(engine)"
   python app.py
   ```

После запуска API будет доступен по адресу `http://127.0.0.1:5000`.

## Основные запросы API

| Метод | Адрес | Описание |
|---|---|---|
| POST | `/auth/signup` | Регистрация |
| POST | `/auth/login` | Получение Access и Refresh Token |
| POST | `/auth/refresh/access` | Обновление Access Token |
| POST | `/auth/refresh/refresh` | Обновление Refresh Token |
| GET | `/user/me` | Информация о себе |
| POST | `/game` | Создание игры |
| POST | `/game/<game_id>` | Выполнение хода |
| GET | `/game/<game_id>` | Получение состояния игры |
| GET | `/games/available` | Список доступных игр |
| POST | `/games/<game_id>/join` | Подключение к игре |
| GET | `/games/history` | История игр пользователя |
| GET | `/games/leaderboard?number=10` | Рейтинг игроков |

Для большинства запросов нужен заголовок `Authorization: Bearer <access_token>`.
В запросах на обновление токена передавайте действующий Refresh Token в JSON:

```json
{
  "refreshToken": "your_refresh_token"
}
```

Пример создания игры против компьютера (`POST /game`):

```json
{
  "is_computer_game": true
}
```

## Структура проекта

- `src/web` — HTTP-маршруты, обработка запросов, проверка токенов.
- `src/domain` — модели и игровая логика.
- `src/datasource` — работа с PostgreSQL.
- `src/di` — настройка зависимостей приложения.
- `src/tests` — тесты.

## Тесты

Из папки `src` выполните:

```bash
python -m pytest tests
```

Часть тестов обращается к PostgreSQL и записывает данные в базу `tic_tac_toe`. Не запускайте их на базе с важными данными.
