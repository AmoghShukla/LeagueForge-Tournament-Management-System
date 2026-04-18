from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.auth import required_role
from src.database.session import get_db
from src.schema.teams import TeamsCreate, TeamsUpdate, TeamsResponse
from src.service.teams import TeamsService

router = APIRouter(prefix="/teams", tags=['Teams'])


@router.post('/', response_model=TeamsResponse)
def create_team(payload: TeamsCreate, db: Session = Depends(get_db),  user = Depends(required_role(['ADMIN']))):
    return TeamsService.create_team(payload, db)


@router.get('/{team_id}', response_model=TeamsResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    return TeamsService.get_team(team_id, db)


@router.get('/', response_model=list[TeamsResponse])
def get_all_teams(db: Session = Depends(get_db)):
    return TeamsService.list_teams(db)


@router.put('/{team_id}', response_model=TeamsResponse)
def update_team(team_id: int, payload: TeamsUpdate, db: Session = Depends(get_db) , user = Depends(required_role(['ADMIN', 'TEAM_OWNER']))):
    return TeamsService.update_team(team_id, payload, db)


@router.delete('/{team_id}')
def delete_team(team_id: int, db: Session = Depends(get_db), user = Depends(required_role(['ADMIN']))):
    return TeamsService.delete_team(team_id, db)
