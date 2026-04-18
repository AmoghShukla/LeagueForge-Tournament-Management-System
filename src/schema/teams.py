from typing import Optional
from pydantic import BaseModel, Field


class TeamsCreate(BaseModel):
    team_name: str = Field(..., min_length=2)
    season_id: int = Field(...)


class TeamsUpdate(BaseModel):
    team_name: Optional[str] = None
    season_id: Optional[int] = None


class TeamsResponse(BaseModel):
    team_id: int
    team_name: str
    season_id: int

    class Config:
        from_attributes = True
