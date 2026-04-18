from sqlalchemy.orm import Session

from src.model.match_result import MatcheResult_Class


class MatchResultRepository:

    @staticmethod
    def get_by_match_id(match_id: int, db: Session) -> MatcheResult_Class | None:
        return db.query(MatcheResult_Class).filter(MatcheResult_Class.match_id == match_id).first()

    @staticmethod
    def upsert(payload: MatcheResult_Class, db: Session) -> MatcheResult_Class:
        existing = db.query(MatcheResult_Class).filter(MatcheResult_Class.match_id == payload.match_id).first()
        if existing:
            existing.toss_winner = payload.toss_winner
            existing.toss_decision = payload.toss_decision
            existing.winner = payload.winner
            existing.result_type = payload.result_type
            db.commit()
            db.refresh(existing)
            return existing

        db.add(payload)
        db.commit()
        db.refresh(payload)
        return payload
