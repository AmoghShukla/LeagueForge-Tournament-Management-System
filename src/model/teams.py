from src.database.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Teams_Class(Base):
    __tablename__="Teams"

    team_id = Column(Integer, primary_key=True, nullable=False)
    team_name = Column(String, nullable=False, unique=True)
    season_id = Column(Integer, nullable=False)

    matches_as_team1 = relationship('Matches_Class',back_populates='team1',foreign_keys='Matches_Class.team1_id')
    matches_as_team2 = relationship(
        'Matches_Class',
        back_populates='team2',
        foreign_keys='Matches_Class.team2_id'
    )
    points = relationship('PointsTable_Class', back_populates='team', uselist=False)