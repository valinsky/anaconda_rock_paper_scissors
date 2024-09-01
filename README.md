[TOC]

# General description
This is a simple Rock Paper Scissor game written purely in Python, and leveraging SQLite and Alembic.

Currently the game supports only 2 players. When the game is run, the two players are prompted to enter their names. Then each playes will take a turn and make a choice. The valid choiced are `rock`, `paper`, `scissors`, `save` and `quit`.
- If a player chooses `save`, the game will end and the current scores will be saved.
- If a player chooses `quit`, that's an indication of a rage quit. The game will not be saved and progress will be lost for both players.
- Otherwise the game will be played normally. The winner of each round will be displayed, alongside their current scores.

# Setup

Python version 3.12.5 needs to be installed on your machine. [Pyenv](https://github.com/pyenv/pyenv) is recommended.

## Create a virutal environment

```
python -m venv .venv
source .venv/bin/activate
```

## Install packages

```
pip install -r requirements/base.txt
```

## Configure Alembic and SQLite

### Initalize alembic
```
alembic init alembic
```

Edit the `alembic/env.py` file:
- Add `from src.models import Base` after the other imports at the top of the file.
- Set `target_metadata = Base.metadata`

### Run migrations
```
make migrations msg="create tables"
make migrate
```

## Play the game

```
python main.py
```
Enjoy!

# Run tests

```
pip install -r requirements/test.txt
```

Run tests using pytest
```
pytest --cov=src tests
```

# Architecture and design
The game is written purely in Python. It uses SQLite as the database, and Alembic for migrations.

The code leverages the MVC pattern, which serves as a basis for a REST API architecture.
The code entry point is the `main()` function found in the root directory's `main.py` file. The `main()` function logically calls a set of functions defined in `src/api.py`. The `api.py` module is an abstracted representantion of REST API endpoints, excluding `api.play()` discussed below.

The game's `main.py` logic (and imagined API calls) can be described like so:
1. Players login via `api.login`.

    The REST equivalent could be:
    - `POST /api/v1/signup` and `POST /api/v1/login`
    - Payload `{"username": "username"}`
    - No password needed currently :)
2. 2 players initiate a game via `api.create_game`:

    The REST equivalent could be:
    - `POST /api/v1/games`
    - Payload `{"user1_id": "user1_id", "user2_id": "user2_id"}`
    - Response: a game id and a session token
3. The 2 players play the game via `api.play`:
    - No REST equivalent in this case. This logic can live on the frontend.
4. The game is finished and progress is potentially saved via `api.save_game` and `api.end_game`:

    The REST equivalent could be:
    - `POST /api/v1/games/{game_id}`
    - Payload `{"user1_score": 4, "user2_score": 2, "save": boolean}`

Models are defined in `src/models.py`. 2 models are defined. A `User` model which contains a user id and a username. A `Game` model which contains a game id, 2 foreign keys to the `User` model representing the 2 players of a game, the individual scores for the players, and a game status, either started or finished. Both models inherit a `TimestampMixin` which define `created_at` and `updated_at` timestamp fields.

Helpers function are defined in `src/utils.py`.

# Future enhancements

1. Enhance the login functionality by using a password. Optional 2 factor auth.
2. Add roles and permissions to users.
3. Have more than 2 players play at the same time.
4. Players have multiple choices besides the basic ones.
5. Spin up a Django or FastAPI server and add REST API endpoints, as described above. Otherwise, AWS Lambda functions can be used.
6. Create a frontend UI that comsumes the APIs. Move `api.play` logic to the frontend.
7. Use a more scalable, secure and feature rich database, like PostgreSQL or DynamoDB.
8. Add CI/CD pipeline.
9. Integration tests.
10. Flake8 and isort.
