import pytest
from unittest.mock import patch

from src.models import User
from src.utils import (
    get_or_create, get_player_choice, determine_winner, init_game_score, print_round_winner,
    print_game_score
)


def test_get_or_create(db_session):
    username = 'username'
    user = get_or_create(User, db_session, name=username)
    assert user.name == username


@pytest.mark.parametrize(
    "input_choice, expected_result",
    [
        ("rock", "rock"),
        ("paper", "paper"),
        ("scissors", "scissors"),
        ("save", "save"),
        ("quit", "quit"),
    ]
)
def test_get_player_choice_valid_input(input_choice, expected_result):
    with patch('builtins.input', side_effect=[input_choice]):
        choice = get_player_choice('Bob')
        assert choice == expected_result


def test_get_player_choice_invalid_input():
    with patch('builtins.input', side_effect=['invalid',]):
        with pytest.raises(StopIteration):
            assert get_player_choice('Bob') is None


@pytest.mark.parametrize(
    "input_choice1, input_choice2, expected_result",
    [
        ("rock", "rock", (0,0)),
        ("rock", "paper", (0,1)),
        ("rock", "scissors", (1,0)),
        ("paper", "paper", (0,0)),
        ("paper", "rock", (1,0)),
        ("paper", "scissors", (0,1)),
        ("scissors", "scissors",(0,0)),
        ("scissors", "rock",(0,1)),
        ("scissors", "paper",(1,0)),
    ]
)
def test_determine_winner(input_choice1, input_choice2, expected_result):
    assert expected_result == determine_winner(input_choice1, input_choice2)


def test_init_game_score():
    game_score = init_game_score()
    assert game_score.user1 == 0
    assert game_score.user2 == 0


@pytest.mark.parametrize(
    "user1_score, user2_score, expected_result",
    [
        (5, 3, "\nusername1 won the round!"),
        (2, 4, "\nusername2 won the round!"),
        (0, 0, "\nIt's a tie!"),
    ]
)
def test_print_round_winner(user1_score, user2_score, expected_result):
    username1 = 'username1'
    username2 = 'username2'
    user1 = User(name=username1)
    user2 = User(name=username2)
    with patch('builtins.print') as mock_print:
        print_round_winner(user1, user2, user1_score, user2_score)
        mock_print.assert_called_once_with(expected_result)


def test_print_game_score():
    username1 = 'username1'
    username2 = 'username2'
    user1 = User(name=username1)
    user2 = User(name=username2)

    user1_score = 5
    user2_score = 7
    game_score = init_game_score()
    game_score.user1 = user1_score
    game_score.user2 = user2_score

    with patch('builtins.print') as mock_print:
        print_game_score(user1, user2, game_score)
        mock_print.assert_called_once_with(
            f"{username1}: {user1_score} - {username2}: {user2_score}")
