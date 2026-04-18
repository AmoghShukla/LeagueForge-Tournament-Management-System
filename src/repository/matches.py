from datetime import date, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.model.matches import Matches_Class


class MatchesRepository:

    @staticmethod
    def create(payload: Matches_Class, db: Session) -> Matches_Class:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        return payload

    @staticmethod
    def get_by_id(match_id: int, db: Session) -> Matches_Class | None:
        return db.query(Matches_Class).filter(Matches_Class.match_id == match_id).first()

    @staticmethod
    def list_all(db: Session) -> list[Matches_Class]:
        return db.query(Matches_Class).order_by(Matches_Class.match_date.asc()).all()

    @staticmethod
    def list_schedule(db: Session) -> list[Matches_Class]:
        return db.query(Matches_Class).order_by(Matches_Class.match_date.asc()).all()

    @staticmethod
    def exists_venue_conflict(venue_id: int, match_date: date, db: Session, exclude_match_id: int | None = None) -> bool:
        query = db.query(Matches_Class).filter(
            Matches_Class.venue_id == venue_id,
            Matches_Class.match_date == match_date
        )
        if exclude_match_id is not None:
            query = query.filter(Matches_Class.match_id != exclude_match_id)
        return query.first() is not None

    @staticmethod
    def list_team_matches_around_date(team_id: int, match_date: date, db: Session, exclude_match_id: int | None = None) -> list[Matches_Class]:
        start_date = match_date - timedelta(days=1)
        end_date = match_date + timedelta(days=1)

        query = db.query(Matches_Class).filter(
            or_(Matches_Class.team1_id == team_id, Matches_Class.team2_id == team_id),
            Matches_Class.match_date >= start_date,
            Matches_Class.match_date <= end_date
        )
        if exclude_match_id is not None:
            query = query.filter(Matches_Class.match_id != exclude_match_id)
        return query.all()

    @staticmethod
    def delete(payload: Matches_Class, db: Session) -> None:
        db.delete(payload)
        db.commit()
