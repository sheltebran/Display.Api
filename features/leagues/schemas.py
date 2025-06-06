from datetime import datetime
from pydantic import BaseModel, ConfigDict

def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')

class LeagueToBeCreated(BaseModel):
    """Schema for a created league."""

    league_id: int
    name: str
    url: str
    sport_id: int
    status: int
    event_date: datetime
    
class CreatedLeague(BaseModel):
    """Schema for a created league with an auto-generated ID."""

    created_league_id: int
    league_id: int
    name: str
    url: str
    sport_id: int
    event_date: datetime
