import pytest
from unittest.mock import patch

from src import constants
from src.api import login, play, create_game, end_game, save_game
from src.models import Game, GameStatus, User
from src.utils import get_or_create, init_game_score


def test_login(db_session):
    player_number = 1
    username = 'username'
    with patch('builtins.input', side_effect=[username]):
        user = login(player_number, db_session)
        assert user.name == username

@pytest.mark.parametrize("user1_choice, user2_choice, save_or_quit, expected_should_save, expected_score_user1, expected_score_user2", [
    (constants.ROCK, constants.SCISSORS, constants.SAVE, True, 1, 0),
    (constants.PAPER, constants.ROCK, constants.SAVE, True, 1, 0),
    (constants.SCISSORS, constants.PAPER, constants.SAVE, True, 1, 0),
    (constants.SCISSORS, constants.ROCK, constants.SAVE, True, 0, 1),
    (constants.ROCK, constants.PAPER, constants.SAVE, True, 0, 1),
    (constants.PAPER, constants.SCISSORS, constants.SAVE, True, 0, 1),
    (constants.ROCK, constants.ROCK, constants.SAVE, True, 0, 0),
    (constants.ROCK, constants.SCISSORS, constants.QUIT, False, 1, 0),
    (constants.PAPER, constants.ROCK, constants.QUIT, False, 1, 0),
    (constants.SCISSORS, constants.PAPER, constants.QUIT, False, 1, 0),
    (constants.SCISSORS, constants.ROCK, constants.QUIT, False, 0, 1),
    (constants.ROCK, constants.PAPER, constants.QUIT, False, 0, 1),
    (constants.PAPER, constants.SCISSORS, constants.QUIT, False, 0, 1),
    (constants.ROCK, constants.ROCK, constants.QUIT, False, 0, 0),
])
def test_play(
        user1_choice, user2_choice, save_or_quit, expected_should_save, expected_score_user1,
        expected_score_user2, db_session, mocker):
    username1 = 'username1'
    username2 = 'username2'
    user1 = get_or_create(User, db_session, name=username1)
    user2 = get_or_create(User, db_session, name=username2)

    mocker.patch(
        'src.api.get_player_choice', 
        side_effect=[user1_choice, user2_choice, save_or_quit,]
    )
    mocker.patch('src.api.print_round_winner')
    mocker.patch('src.api.print_game_score')

    should_save, game_score = play(user1, user2)
    assert should_save == expected_should_save
    assert game_score.user1 == expected_score_user1
    assert game_score.user2 == expected_score_user2



def test_create_game(db_session):
    username1 = 'username1'
    username2 = 'username2'
    user1 = get_or_create(User, db_session, name=username1)
    user2 = get_or_create(User, db_session, name=username2)
    game = create_game(user1, user2, db_session)
    assert game.status == GameStatus.STARTED
    assert game.user1 == user1
    assert game.user2 == user2
    assert game.user1_score == 0
    assert game.user1_score == 0


def test_save_game(db_session):
    username1 = 'username1'
    username2 = 'username2'
    user1 = get_or_create(User, db_session, name=username1)
    user2 = get_or_create(User, db_session, name=username2)
    game = create_game(user1, user2, db_session)
    game_score = init_game_score()
    game_score.user1 = 2
    game_score.user2 = 3
    save_game(game, game_score, db_session)
    saved_game = get_or_create(Game, db_session, id=game.id)
    assert saved_game.user1_score == 2
    assert saved_game.user2_score == 3



def test_end_game(db_session):
    username1 = 'username1'
    username2 = 'username2'
    user1 = get_or_create(User, db_session, name=username1)
    user2 = get_or_create(User, db_session, name=username2)
    game = create_game(user1, user2, db_session)
    end_game(game, db_session)
    saved_game = get_or_create(Game, db_session, id=game.id)
    assert saved_game.status == GameStatus.FINISHED
