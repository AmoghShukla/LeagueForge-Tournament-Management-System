from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
from src.model.enum import MatchStatus, TossDecision, ResultType


class MatchesCreate(BaseModel):
    season_id: int = Field(...)
    team1_id: int = Field(...)
    team2_id: int = Field(...)
    venue_id: int = Field(...)
    match_date: date = Field(...)

class MatchesUpdate(BaseModel):
    season_id: Optional[int] = None
    team1_id: Optional[int] = None
    team2_id: Optional[int] = None
    venue_id: Optional[int] = None
    match_date: Optional[date] = None

class MatchesResponse(BaseModel):
    match_id: int
    season_id: int
    team1_id: int
    team2_id: int
    venue_id: int
    match_date: date
    match_status: MatchStatus

    class Config:
        from_attributes = True


class MatchResultCreate(BaseModel):
    toss_winner: int
    toss_decision: TossDecision = TossDecision.BATTING
    winner: Optional[int] = None
    result_type: ResultType = ResultType.COMPLETED


class MatchResultResponse(BaseModel):
    matchresult_id: int
    match_id: int
    toss_winner: int
    toss_decision: TossDecision
    winner: Optional[int] = None
    result_type: ResultType

    class Config:
        from_attributes = True


class ScheduleResponse(BaseModel):
    match_id: int
    season_id: int
    team1_id: int
    team2_id: int
    venue_id: int
    match_date: date
    match_status: MatchStatus

    class Config:
        from_attributes = True
