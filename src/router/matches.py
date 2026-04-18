from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.auth import required_role
from src.database.session import get_db
from src.schema.matches import (
    MatchResultCreate,
    MatchResultResponse,
    MatchesCreate,
    MatchesUpdate,
    MatchesResponse,
    ScheduleResponse,
)
from src.schema.points import PointsTableResponse
from src.service.matches import MatchesService

router = APIRouter(prefix="/matches", tags=['Matches'])


@router.post('/', response_model=MatchesResponse)
def create_match(payload: MatchesCreate, db: Session = Depends(get_db), user = Depends(required_role(['ADMIN']))):
    return MatchesService.create_match(payload, db)


@router.get('/schedule', response_model=list[ScheduleResponse])
def get_schedule(db: Session = Depends(get_db)):
    return MatchesService.get_schedule(db)


@router.get('/points-table/{season_id}', response_model=list[PointsTableResponse])
def get_points_table(season_id: int, db: Session = Depends(get_db)):
    return MatchesService.get_points_table(season_id, db)


@router.post('/{match_id}/result', response_model=MatchResultResponse)
def record_match_result(match_id: int, payload: MatchResultCreate, db: Session = Depends(get_db), user = Depends(required_role(['SCORE_UPDATER']))):
    return MatchesService.record_result(match_id, payload, db)


@router.get('/{match_id}', response_model=MatchesResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    return MatchesService.get_match(match_id, db)


@router.get('/', response_model=list[MatchesResponse])
def get_all_matches(db: Session = Depends(get_db)):
    return MatchesService.list_matches(db)


@router.put('/{match_id}', response_model=MatchesResponse)
def update_match(match_id: int, payload: MatchesUpdate, db: Session = Depends(get_db), user = Depends(required_role(['ADMIN']))):
    return MatchesService.update_match(match_id, payload, db)


@router.delete('/{match_id}')
def delete_match(match_id: int, db: Session = Depends(get_db), user = Depends(required_role(['ADMIN']))):
    return MatchesService.delete_match(match_id, db)
