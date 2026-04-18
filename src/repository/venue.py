from sqlalchemy.orm import Session

from src.model.venue import Venue_Class


class VenueRepository:

    @staticmethod
    def create(payload: Venue_Class, db: Session) -> Venue_Class:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        return payload

    @staticmethod
    def get_by_id(venue_id: int, db: Session) -> Venue_Class | None:
        return db.query(Venue_Class).filter(Venue_Class.venue_id == venue_id).first()

    @staticmethod
    def get_by_name(venue_name: str, db: Session) -> Venue_Class | None:
        return db.query(Venue_Class).filter(Venue_Class.venue_name == venue_name).first()

    @staticmethod
    def list_all(db: Session) -> list[Venue_Class]:
        return db.query(Venue_Class).all()

    @staticmethod
    def delete(payload: Venue_Class, db: Session) -> None:
        db.delete(payload)
        db.commit()
