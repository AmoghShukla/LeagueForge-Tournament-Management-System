from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.model.venue import Venue_Class
from src.repository.venue import VenueRepository


class VenueService:

    @staticmethod
    def create_venue(payload, db: Session):
        existing = VenueRepository.get_by_name(payload.venue_name, db)
        if existing:
            raise HTTPException(status_code=400, detail='Venue already exists')

        venue = Venue_Class(
            venue_name=payload.venue_name,
            venue_address=payload.venue_address,
            venue_capacity=payload.venue_capacity,
        )
        return VenueRepository.create(venue, db)

    @staticmethod
    def get_venue(venue_id: int, db: Session):
        venue = VenueRepository.get_by_id(venue_id, db)
        if not venue:
            raise HTTPException(status_code=404, detail='Venue not found')
        return venue

    @staticmethod
    def list_venues(db: Session):
        return VenueRepository.list_all(db)

    @staticmethod
    def update_venue(venue_id: int, payload, db: Session):
        venue = VenueRepository.get_by_id(venue_id, db)
        if not venue:
            raise HTTPException(status_code=404, detail='Venue not found')

        if payload.venue_name and payload.venue_name != venue.venue_name:
            duplicate = VenueRepository.get_by_name(payload.venue_name, db)
            if duplicate:
                raise HTTPException(status_code=400, detail='Venue name already exists')
            venue.venue_name = payload.venue_name

        if payload.venue_address is not None:
            venue.venue_address = payload.venue_address
        if payload.venue_capacity is not None:
            venue.venue_capacity = payload.venue_capacity

        db.commit()
        db.refresh(venue)
        return venue

    @staticmethod
    def delete_venue(venue_id: int, db: Session):
        venue = VenueRepository.get_by_id(venue_id, db)
        if not venue:
            raise HTTPException(status_code=404, detail='Venue not found')
        VenueRepository.delete(venue, db)
        return {'message': 'Venue deleted successfully'}
