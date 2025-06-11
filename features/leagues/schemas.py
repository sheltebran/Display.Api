from datetime import datetime
from pydantic import BaseModel

class LeagueToBeCreated(BaseModel):
    """Schema for league data received from RabbitMQ."""

    league_id: int
    name: str
    url: str
    sport_id: int
    status: int
    event_date: str
    
class CreatedLeague(BaseModel):
    """Schema for a created league with an auto-generated ID."""

    created_league_id: int
    league_id: int
    name: str
    url: str
    sport_id: int
    event_date: datetime
