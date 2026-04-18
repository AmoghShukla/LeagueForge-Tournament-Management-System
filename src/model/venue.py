from sqlalchemy.orm import relationship

from src.database.base import Base
from sqlalchemy import Column, Integer, String

class Venue_Class(Base):
    __tablename__="Venue"

    venue_id = Column(Integer, primary_key=True, nullable=False)
    venue_name = Column(String, nullable=False, unique=True)
    venue_address = Column(String)
    venue_capacity = Column('Venue_Capacity', Integer)

    venue_availability = relationship('Venue_Availability_Class', back_populates='venue')
    matches = relationship('Matches_Class', back_populates='venue')