import pytest

from src.db import Session


@pytest.fixture(scope='function')
def db_session():
    """
    Create a new database session for a test.
    """
    # Create a new session
    session = Session()
    yield session

    # Remove the session after the test
    session.close()
