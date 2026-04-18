from sqlalchemy.orm import Session

from src.model.points import PointsTable_Class


class PointsRepository:

    @staticmethod
    def get_or_create(team_id: int, season_id: int, db: Session) -> PointsTable_Class:
        row = db.query(PointsTable_Class).filter(
            PointsTable_Class.team_id == team_id,
            PointsTable_Class.season_id == season_id
        ).first()
        if row:
            return row

        row = PointsTable_Class(team_id=team_id, season_id=season_id)
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def list_by_season(season_id: int, db: Session) -> list[PointsTable_Class]:
        return db.query(PointsTable_Class).filter(
            PointsTable_Class.season_id == season_id
        ).order_by(
            PointsTable_Class.points.desc(),
            PointsTable_Class.won.desc()
        ).all()

    @staticmethod
    def reset_season_stats(season_id: int, db: Session) -> None:
        rows = db.query(PointsTable_Class).filter(PointsTable_Class.season_id == season_id).all()
        for row in rows:
            row.played = 0
            row.won = 0
            row.lost = 0
            row.no_result = 0
            row.points = 0

    @staticmethod
    def save(db: Session) -> None:
        db.commit()
