from typing import Tuple
from types import SimpleNamespace

from sqlalchemy.orm.session import Session as SQLAlchemySession

from . import constants
from .exceptions import LoginException
from .models import User, Game, GameStatus
from .utils import (
    get_or_create, init_game_score, get_player_choice, determine_winner, print_round_winner,
    print_game_score
)


def login(player_number: int, session: 'SQLAlchemySession') -> 'User':
    """
    Return the User object based on player input. If object doesn't exist in the db, create it.
    :param player: Player number.
    :param session: The DB session.
    :return: User object
    """
    try:
        username = input(f"Player {player_number} name: ")
        return get_or_create(User, session, name=username)
    except Exception as exception:
        raise LoginException(f"Exception during login: {exception}")


def create_game(user1: 'User', user2: 'User', session: 'SQLAlchemySession') -> 'Game':
    """
    Create a new game session.
    :param user1: User object.
    :param user2: User object.
    :param session: DB session.
    :return: A new Game object.
    """
    game = Game(user1=user1, user2=user2)
    session.add(game)
    session.commit()
    return game


def end_game(game: 'Game', session: 'SQLAlchemySession') -> None:
    """
    Set the Game object status to FINISHED.
    :param game: Game object.
    :param session: DB session.
    """
    game.status = GameStatus.FINISHED.value
    session.commit()


def play(user1: 'User', user2: 'User') -> Tuple[bool, SimpleNamespace]:
    """
    The main logic of the rock-paper-scissors game. Players are prompted to enter their choices
    until one of them either saves or quits. The score is displayed after every round.
    This logic can be moved to the front-end.
    :param user1: User object.
    :param user2: User object.
    :return: Tuple containing a bool denoting if game should be saved,
        and a SimpleNamespace that keeps track of the score for both users
    """
    game_score = init_game_score()
    while True:
        print()
        user1_choice = get_player_choice(user1.name)
        if user1_choice == constants.SAVE:
            return True, game_score
        if user1_choice == constants.QUIT:
            print(f"\n{user1.name} rage quit.\nNot saving.")
            return False, game_score

        user2_choice = get_player_choice(user2.name)
        if user2_choice == constants.SAVE:
            return True, game_score
        if user2_choice == constants.QUIT:
            print(f"\n{user2.name} rage quit.\nNot saving.")
            return False, game_score

        user1_round_score, user2_round_score = determine_winner(user1_choice, user2_choice)
        print_round_winner(user1, user2, user1_round_score, user2_round_score)
        game_score.user1 += user1_round_score
        game_score.user2 += user2_round_score
        print_game_score(user1, user2, game_score)


def save_game(game: 'Game', game_score: 'SimpleNamespace', session: 'SQLAlchemySession') -> None:
    """
    Update the game score for both users in the DB.
    :param game: Game object.
    :param game_score: SimpleNamespace that keeps track of the score.
    :param session: DB session.
    """
    print(f"\nFinal score is {game.user1.name}: {game_score.user1} - {game.user2.name}: {game_score.user2}")
    print(f"Saving.")
    game.user1_score = game_score.user1
    game.user2_score = game_score.user2
    session.commit()
