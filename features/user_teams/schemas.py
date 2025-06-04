from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserTeamToBeCreated(BaseModel):
    """Schema for a created user team."""

    model_config = ConfigDict(populate_by_name=True)

    user_team_id: str  # UUID as string
    name: str
    starting_amount: int
    is_paid: bool
    is_active: bool
    slogan: str | None = None
    email: str
    season_id: str  # UUID as string
    user_id: str  # UUID as string
    status: str  # Assuming CreatedStatus is a string enum or similar
    event_date: datetime

    @classmethod
    def aliases(cls):
        """Return a dictionary of field aliases."""

        return {
            "user_team_id": "userTeamId",
            "name": "name",
            "starting_amount": "startingAmount",
            "is_paid": "isPaid",
            "is_active": "isActive",
            "slogan": "slogan",
            "email": "email",
            "season_id": "seasonId",
            "user_id": "userId",
            "status": "status",
            "event_date": "eventDate"
        }
    
class CreatedUserTeam(BaseModel):
    """Schema for a created league with an auto-generated ID."""

    created_user_team_id: int    
    user_team_id: str  # UUID as string
    name: str
    starting_amount: int
    is_paid: bool
    is_active: bool
    slogan: str | None = None
    email: str
    season_id: str  # UUID as string
    user_id: str  # UUID as string
    event_date: datetime

