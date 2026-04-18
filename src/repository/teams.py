from sqlalchemy.orm import Session
from src.model.teams import Teams_Class


class TeamsRepository:

    @staticmethod
    def create(payload: Teams_Class, db: Session) -> Teams_Class:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        return payload

    @staticmethod
    def get_by_id(team_id: int, db: Session) -> Teams_Class | None:
        return db.query(Teams_Class).filter(Teams_Class.team_id == team_id).first()

    @staticmethod
    def get_by_name(team_name: str, db: Session) -> Teams_Class | None:
        return db.query(Teams_Class).filter(Teams_Class.team_name == team_name).first()

    @staticmethod
    def list_all(db: Session) -> list[Teams_Class]:
        return db.query(Teams_Class).all()

    @staticmethod
    def delete(payload: Teams_Class, db: Session) -> None:
        db.delete(payload)
        db.commit()
