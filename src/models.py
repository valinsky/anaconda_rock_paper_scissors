import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class TimestampMixin(Base):
    __abstract__ = True  # This class will not create a table

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class User(TimestampMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class GameStatus(enum.Enum):
    STARTED = "STARTED"
    FINISHED = "FINISHED"


class Game(TimestampMixin):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user2_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user1_score = Column(Integer, default=0)
    user2_score = Column(Integer, default=0)
    status = Column(Enum(GameStatus), nullable=False, default=GameStatus.STARTED)

    # Relationship to User
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
