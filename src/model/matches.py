from sqlalchemy.orm import relationship

from src.database.base import Base

from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, UniqueConstraint, Enum as SQLAlchemyEnum
from src.model.enum import MatchStatus

class Matches_Class(Base):
    __tablename__="Match"

    match_id = Column(Integer, primary_key=True, nullable=False)
    season_id = Column(Integer, nullable=False)
    team1_id = Column(Integer, ForeignKey('Teams.team_id'), nullable=False)
    team2_id = Column(Integer, ForeignKey('Teams.team_id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('Venue.venue_id'), nullable=False)
    match_date = Column(Date, nullable=False)
    match_status = Column(SQLAlchemyEnum(MatchStatus), default=MatchStatus.YET_TO_START)

    team1 = relationship('Teams_Class', foreign_keys=[team1_id], back_populates='matches_as_team1')
    team2 = relationship('Teams_Class', foreign_keys=[team2_id], back_populates='matches_as_team2')
    venue = relationship('Venue_Class', back_populates='matches')
    result = relationship('MatcheResult_Class', back_populates='match', uselist=False)
