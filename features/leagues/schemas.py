from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LeagueToBeCreated(BaseModel):
    """Schema for a created league."""

    model_config = ConfigDict(populate_by_name=True)

    league_id: int
    name: str
    url: str
    sport_id: int
    status: int
    event_date: datetime

    @classmethod
    def aliases(cls):
        """Return a dictionary of field aliases."""

        return {
            "league_id": "leagueId",
            "name": "name",
            "url": "url",
            "sport_id": "sportId",
            "status": "status",
            "event_date": "eventDate"
        }
    
class CreatedLeague(BaseModel):
    """Schema for a created league with an auto-generated ID."""

    created_league_id: int
    league_id: int
    name: str
    url: str
    sport_id: int
    event_date: datetime
