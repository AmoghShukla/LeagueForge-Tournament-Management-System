from src.database.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from src.model.enum import TossDecision, ResultType

class MatcheResult_Class(Base):
    __tablename__="MatchResult"

    matchresult_id = Column(Integer, primary_key=True, nullable=False)
    match_id = Column(Integer, ForeignKey('Match.match_id'), nullable=False, unique=True)
    toss_winner = Column(Integer, nullable=False)
    toss_decision = Column(SQLAlchemyEnum(TossDecision), default=TossDecision.BATTING)
    winner = Column(Integer, default=None)
    result_type = Column(SQLAlchemyEnum(ResultType), default=ResultType.COMPLETED)

    match = relationship('Matches_Class', back_populates='result')
