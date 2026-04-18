from pydantic import BaseModel


class PointsTableResponse(BaseModel):
    team_id: int
    team_name: str
    season_id: int
    played: int
    won: int
    lost: int
    no_result: int
    points: int
