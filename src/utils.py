from types import SimpleNamespace
from typing import Tuple, Any

from sqlalchemy.orm.session import Session as SQLAlchemySession

from . import constants


def get_or_create(model: Any, session: 'SQLAlchemySession', **kwargs) -> Any:
    """
    Get a DB object based on **kwargs. If obj not present in DB, create it.
    :param model: DB model.
    :session: DB session.
    :kwargs: params used in the filter query.
    """
    obj = session.query(model).filter_by(**kwargs).first()
    if not obj:
        obj = model(**kwargs)
        session.add(obj)
        session.commit()
    return obj


def get_player_choice(username: str) -> str:
    """
    Player has to pick one of the valid choices.
    Otherwise player will continue to be prompted for a choice.
    :param username: Name of the user.
    :return: Choice inputed by user.
    """
    while True:
        choice = input(f"{username} choice: ").strip().lower()
        if choice in constants.VALID_CHOICES:
            return choice
        print(f"Invalid input. Please enter one of {constants.VALID_CHOICES}")


def determine_winner(choice1: str, choice2: str) -> Tuple[int, int]:
    """
    Determine the winner based on the choices.
    Return a tuple with the score for each choice.
    :param choice1: Choice made by player1.
    :param choice2: Choice made by player2.
    :return: Tuple containg the winning choice.
    """
    if choice1 == choice2:
        return (0, 0)
    if (choice1 == constants.ROCK and choice2 == constants.SCISSORS) or \
        (choice1 == constants.SCISSORS and choice2 == constants.PAPER) or \
        (choice1 == constants.PAPER and choice2 == constants.ROCK):
        return (1, 0)
    return (0, 1)


def init_game_score() -> 'SimpleNamespace':
    """
    Initialize a SimpleNamespace that holds the players score for the duration of a game.
    :return: SimpleNamespace
    """
    game_score = SimpleNamespace()
    game_score.user1 = 0
    game_score.user2 = 0
    return game_score


def print_round_winner(user1, user2, user1_round_score, user2_round_score) -> None:
    """
    Calculate the winner and print a message.
    :param user1: User object.
    :param user2: User object.
    :param user1_round_score: User1 score for the current round.
    :param user2_round_score: User2 score for the current round.
    """
    message = constants.ITS_A_TIE_MESSAGE
    if user1_round_score > user2_round_score:
        message = constants.ROUND_WINNER_MESSAGE.format(winner=user1.name)
    elif user1_round_score < user2_round_score:
        message = constants.ROUND_WINNER_MESSAGE.format(winner=user2.name)
    print(f"\n{message}")


def print_game_score(user1, user2, score) -> None:
    """
    Print the current score between the players.
    :param user1: User object.
    :param user2: User object.
    :param score: SimpleNamespace that holds the players game score.
    """
    print(f"{user1.name}: {score.user1} - {user2.name}: {score.user2}")
