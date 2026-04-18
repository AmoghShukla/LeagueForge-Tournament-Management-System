from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.model.teams import Teams_Class
from src.repository.teams import TeamsRepository


class TeamsService:

    @staticmethod
    def create_team(payload, db: Session):
        existing = TeamsRepository.get_by_name(payload.team_name, db)
        if existing:
            raise HTTPException(status_code=400, detail='Team already exists')

        team = Teams_Class(team_name=payload.team_name, season_id=payload.season_id)
        return TeamsRepository.create(team, db)

    @staticmethod
    def get_team(team_id: int, db: Session):
        team = TeamsRepository.get_by_id(team_id, db)
        if not team:
            raise HTTPException(status_code=404, detail='Team not found')
        return team

    @staticmethod
    def list_teams(db: Session):
        return TeamsRepository.list_all(db)

    @staticmethod
    def update_team(team_id: int, payload, db: Session):
        team = TeamsRepository.get_by_id(team_id, db)
        if not team:
            raise HTTPException(status_code=404, detail='Team not found')

        if payload.team_name and payload.team_name != team.team_name:
            duplicate = TeamsRepository.get_by_name(payload.team_name, db)
            if duplicate:
                raise HTTPException(status_code=400, detail='Team name already exists')
            team.team_name = payload.team_name

        if payload.season_id is not None:
            team.season_id = payload.season_id

        db.commit()
        db.refresh(team)
        return team

    @staticmethod
    def delete_team(team_id: int, db: Session):
        team = TeamsRepository.get_by_id(team_id, db)
        if not team:
            raise HTTPException(status_code=404, detail='Team not found')
        TeamsRepository.delete(team, db)
        return {'message': 'Team deleted successfully'}
