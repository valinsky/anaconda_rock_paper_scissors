from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import constants


# Database setup
engine = create_engine(constants.DATABASE_URL)
Session = sessionmaker(bind=engine)
# Base.metadata.create_all(bind=engine)
