from datetime import datetime
from pydantic import BaseModel

# class DefaultPickToBeCreated(BaseModel):
#     """Schema for a created default pick."""

#     game_id: int
#     favorite_team_id: str
#     favorite_team_name: str
#     spread: float
#     week_id: int | None = None
#     week_number: int
#     status: str  # Assuming CreatedStatus is a string enum or similar
#     event_date: str # ISO format date string
    
class CreatedDefaultPick(BaseModel):
    """Schema for a created default pick with an auto-generated ID."""

    created_default_pick_id: int
    bet: int
    game_id: int
    favorite_team_id: str
    favorite_team_name: str
    spread: float
    week_id: int
    week_number: int
    event_date: datetime

