from src.database.base import Base
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship


class PointsTable_Class(Base):
	__tablename__ = "PointsTable"
	

	points_id = Column(Integer, primary_key=True, nullable=False)
	team_id = Column(Integer, ForeignKey('Teams.team_id'), nullable=False)
	season_id = Column(Integer, nullable=False)
	played = Column(Integer, nullable=False, default=0)
	won = Column(Integer, nullable=False, default=0)
	lost = Column(Integer, nullable=False, default=0)
	no_result = Column(Integer, nullable=False, default=0)
	points = Column(Integer, nullable=False, default=0)

	team = relationship('Teams_Class', back_populates='points')
