from typing import Optional
from pydantic import BaseModel, Field


class VenueCreate(BaseModel):
    venue_name: str = Field(..., min_length=2)
    venue_address: Optional[str] = None
    venue_capacity: Optional[int] = None


class VenueUpdate(BaseModel):
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    venue_capacity: Optional[int] = None


class VenueResponse(BaseModel):
    venue_id: int
    venue_name: str
    venue_address: Optional[str] = None
    venue_capacity: Optional[int] = None

    class Config:
        from_attributes = True
