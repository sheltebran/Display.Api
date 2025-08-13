from datetime import datetime
from pydantic import BaseModel

# class WeekToBeCreated(BaseModel):
#     """Schema for a created week."""

#     week_id: int
#     week_number: int
#     start_date: str # ISO format date string
#     end_date: str # ISO format date string
#     deadline_date: str | None = None
#     season_id: str  # UUID as string
#     status: str  # Assuming CreatedStatus is a string enum or similar
#     event_date: str # ISO format date string
    
class CreatedWeek(BaseModel):
    """Schema for a created league with an auto-generated ID."""

    created_user_team_id: int    
    week_id: int
    week_number: int
    start_date: datetime
    end_date: datetime
    deadline_date: datetime
    season_id: str  # UUID as string
    event_date: datetime

