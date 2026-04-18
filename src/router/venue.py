from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.auth import required_role
from src.database.session import get_db
from src.schema.venue import VenueCreate, VenueUpdate, VenueResponse
from src.service.venue import VenueService

router = APIRouter(prefix="/venue", tags=['Venue'])


@router.post('/', response_model=VenueResponse)
def create_venue(payload: VenueCreate, db: Session = Depends(get_db),user = Depends(required_role(['ADMIN', 'VENUE_MANAGER']))):
    return VenueService.create_venue(payload, db)


@router.get('/{venue_id}', response_model=VenueResponse)
def get_venue(venue_id: int, db: Session = Depends(get_db)):
    return VenueService.get_venue(venue_id, db)


@router.get('/', response_model=list[VenueResponse])
def get_all_venues(db: Session = Depends(get_db)):
    return VenueService.list_venues(db)


@router.put('/{venue_id}', response_model=VenueResponse)
def update_venue(venue_id: int, payload: VenueUpdate, db: Session = Depends(get_db), user = Depends(required_role(['ADMIN', 'VENUE_MANAGER']))):
    return VenueService.update_venue(venue_id, payload, db)


@router.delete('/{venue_id}')
def delete_venue(venue_id: int, db: Session = Depends(get_db), user = Depends(required_role(['ADMIN']))):
    return VenueService.delete_venue(venue_id, db)
