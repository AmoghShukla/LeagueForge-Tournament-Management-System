
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.model.match_result import MatcheResult_Class
from src.model.matches import Matches_Class
from src.model.enum import MatchStatus, ResultType
from src.repository.match_result import MatchResultRepository
from src.repository.matches import MatchesRepository
from src.repository.points import PointsRepository
from src.repository.teams import TeamsRepository
from src.repository.venue import VenueRepository


class MatchesService:

    @staticmethod
    def _validate_schedule_rules(payload, db: Session, exclude_match_id: int | None = None) -> None:
        if payload.team1_id == payload.team2_id:
            raise HTTPException(status_code=400, detail='A team cannot play against itself')

        if not TeamsRepository.get_by_id(payload.team1_id, db):
            raise HTTPException(status_code=404, detail='Team 1 not found')
        if not TeamsRepository.get_by_id(payload.team2_id, db):
            raise HTTPException(status_code=404, detail='Team 2 not found')
        if not VenueRepository.get_by_id(payload.venue_id, db):
            raise HTTPException(status_code=404, detail='Venue not found')

        if MatchesRepository.exists_venue_conflict(
            payload.venue_id,
            payload.match_date,
            db,
            exclude_match_id=exclude_match_id,
        ):
            raise HTTPException(status_code=400, detail='Venue conflict on this date')

        team1_near_matches = MatchesRepository.list_team_matches_around_date(
            payload.team1_id,
            payload.match_date,
            db,
            exclude_match_id=exclude_match_id,
        )
        if team1_near_matches:
            raise HTTPException(
                status_code=400,
                detail='Team 1 must have at least a 2-day gap before playing again',
            )

        team2_near_matches = MatchesRepository.list_team_matches_around_date(
            payload.team2_id,
            payload.match_date,
            db,
            exclude_match_id=exclude_match_id,
        )
        if team2_near_matches:
            raise HTTPException(
                status_code=400,
                detail='Team 2 must have at least a 2-day gap before playing again',
            )

    @staticmethod
    def create_match(payload, db: Session):
        MatchesService._validate_schedule_rules(payload, db)

        match = Matches_Class(
            season_id=payload.season_id,
            team1_id=payload.team1_id,
            team2_id=payload.team2_id,
            venue_id=payload.venue_id,
            match_date=payload.match_date,
            match_status=MatchStatus.YET_TO_START,
        )
        return MatchesRepository.create(match, db)

    @staticmethod
    def update_match(match_id: int, payload, db: Session):
        match = MatchesRepository.get_by_id(match_id, db)
        if not match:
            raise HTTPException(status_code=404, detail='Match not found')

        match.season_id = payload.season_id if payload.season_id is not None else match.season_id
        match.team1_id = payload.team1_id if payload.team1_id is not None else match.team1_id
        match.team2_id = payload.team2_id if payload.team2_id is not None else match.team2_id
        match.venue_id = payload.venue_id if payload.venue_id is not None else match.venue_id
        match.match_date = payload.match_date if payload.match_date is not None else match.match_date

        MatchesService._validate_schedule_rules(match, db, exclude_match_id=match_id)
        db.commit()
        db.refresh(match)
        return match

    @staticmethod
    def get_match(match_id: int, db: Session):
        match = MatchesRepository.get_by_id(match_id, db)
        if not match:
            raise HTTPException(status_code=404, detail='Match not found')
        return match

    @staticmethod
    def list_matches(db: Session):
        return MatchesRepository.list_all(db)

    @staticmethod
    def delete_match(match_id: int, db: Session):
        match = MatchesRepository.get_by_id(match_id, db)
        if not match:
            raise HTTPException(status_code=404, detail='Match not found')
        MatchesRepository.delete(match, db)
        return {'message': 'Match deleted successfully'}

    @staticmethod
    def get_schedule(db: Session):
        return MatchesRepository.list_schedule(db)

    @staticmethod
    def record_result(match_id: int, payload, db: Session):
        match = MatchesRepository.get_by_id(match_id, db)
        if not match:
            raise HTTPException(status_code=404, detail='Match not found')

        valid_winners = {match.team1_id, match.team2_id}
        if payload.result_type == ResultType.COMPLETED and payload.winner not in valid_winners:
            raise HTTPException(status_code=400, detail='Winner must be one of the playing teams')

        result = MatcheResult_Class(
            match_id=match.match_id,
            toss_winner=payload.toss_winner,
            toss_decision=payload.toss_decision,
            winner=payload.winner,
            result_type=payload.result_type,
        )
        saved = MatchResultRepository.upsert(result, db)

        if payload.result_type == ResultType.COMPLETED:
            match.match_status = MatchStatus.STARTED
        else:
            match.match_status = MatchStatus.ABANDONED
        db.commit()

        
        PointsRepository.get_or_create(match.team1_id, match.season_id, db)
        PointsRepository.get_or_create(match.team2_id, match.season_id, db)
        PointsRepository.reset_season_stats(match.season_id, db)

        all_matches = MatchesRepository.list_all(db)
        for m in all_matches:
            if m.season_id != match.season_id:
                continue
            existing_result = MatchResultRepository.get_by_match_id(m.match_id, db)
            if not existing_result:
                continue

            p1 = PointsRepository.get_or_create(m.team1_id, m.season_id, db)
            p2 = PointsRepository.get_or_create(m.team2_id, m.season_id, db)

            p1.played += 1
            p2.played += 1

            if existing_result.result_type == ResultType.COMPLETED and existing_result.winner:
                if existing_result.winner == m.team1_id:
                    p1.won += 1
                    p1.points += 2
                    p2.lost += 1
                else:
                    p2.won += 1
                    p2.points += 2
                    p1.lost += 1
            else:
                p1.no_result += 1
                p2.no_result += 1
                p1.points += 1
                p2.points += 1

        PointsRepository.save(db)
        return saved

    @staticmethod
    def get_points_table(season_id: int, db: Session):
        rows = PointsRepository.list_by_season(season_id, db)
        return [
            {
                'team_id': row.team_id,
                'team_name': row.team.team_name if row.team else '',
                'season_id': row.season_id,
                'played': row.played,
                'won': row.won,
                'lost': row.lost,
                'no_result': row.no_result,
                'points': row.points,
            }
            for row in rows
        ]