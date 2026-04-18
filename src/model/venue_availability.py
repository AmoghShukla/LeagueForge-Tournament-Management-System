from sqlalchemy.orm import relationship

from src.database.base import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, UniqueConstraint

class Venue_Availability_Class(Base):
    __tablename__="Venue_Avaialability"

    venue_availability_id = Column(Integer, primary_key=True, nullable=False)
    venue_id = Column(Integer, ForeignKey('Venue.venue_id'), nullable=False)
    venue_availability_date = Column(Date, nullable=False)

    venue = relationship('Venue_Class', back_populates='venue_availability')

