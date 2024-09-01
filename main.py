from src.db import Session
from src import api


def main():
    """
    Entry point into the rock-paper-scissors game.
    """
    # Create DB session
    session = Session()

    # Login the users
    user1 = api.login(player_number=1, session=session)
    user2 = api.login(player_number=2, session=session)

    # Start a new game
    game = api.create_game(user1, user2, session)

    # Play the game
    should_save, game_score = api.play(user1, user2)

    # Save the game if needed
    if should_save:
        api.save_game(game, game_score, session)

    # Close the game and DB session
    api.end_game(game, session)
    session.close()

if __name__ == '__main__':
    main()
