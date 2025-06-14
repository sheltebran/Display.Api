from datetime import datetime
from pydantic import BaseModel

class UserTeamToBeCreated(BaseModel):
    """Schema for a created user team."""

    user_team_id: str  # UUID as string
    name: str
    starting_amount: int
    is_paid: bool
    payment_reference: str | None = None
    is_active: bool
    slogan: str | None = None
    email: str
    season_id: str  # UUID as string
    user_id: str  # UUID as string
    status: str  # Assuming CreatedStatus is a string enum or similar
    event_date: str
    
class CreatedUserTeam(BaseModel):
    """Schema for a created league with an auto-generated ID."""

    created_user_team_id: int    
    user_team_id: str  # UUID as string
    name: str
    starting_amount: int
    is_paid: bool
    payment_reference: str | None = None
    is_active: bool
    slogan: str | None = None
    email: str
    season_id: str  # UUID as string
    user_id: str  # UUID as string
    event_date: datetime

