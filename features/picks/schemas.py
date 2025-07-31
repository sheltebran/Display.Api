from datetime import datetime
from pydantic import BaseModel
from typing import List

class PickDetailToBeCreated(BaseModel):
    """Schema for pick detail data received from RabbitMQ."""
    
    pick_detail_id: int
    game_id: int
    spread: float
    total: float
    is_correct: int  # PickWin enum value
    pick_id: int
    football_team_id: str

class PickToBeCreated(BaseModel):
    """Schema for pick data received from RabbitMQ."""
    
    pick_id: int
    bet: int
    amount_won: int
    week_id: int
    user_team_id: str  # UUID as string
    pick_details: List[PickDetailToBeCreated]
    status: int  # CreatedStatus enum value
    event_date: str  # ISO format date string

class CreatedPickDetail(BaseModel):
    """Schema for a created pick detail with an auto-generated ID."""
    
    created_pick_detail_id: int
    pick_detail_id: int
    game_id: int
    spread: float
    total: float
    is_correct: int  # PickWin enum value
    created_pick_id: int  # Foreign key to created_picks
    football_team_id: str
    event_date: datetime

class CreatedPick(BaseModel):
    """Schema for a created pick with an auto-generated ID."""
    
    created_pick_id: int
    pick_id: int
    bet: int
    amount_won: int
    week_id: int
    user_team_id: str  # UUID as string
    parlay_size: int
    event_date: datetime
