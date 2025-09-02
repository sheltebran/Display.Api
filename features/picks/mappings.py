from core.date_helpers import format_date
from features.picks.schemas import (
    CreatedPick,
    CreatedPickDetail
)
from typing import List

def map_to_created_pick(pick_data: dict) -> CreatedPick:
    """Map a pick dictionary to a CreatedPick object.
    
    Parameters
    ----------
    pick_data : dict
        Data dictionary containing pick information from RabbitMQ.
    
    Returns
    -------
    CreatedPick
        A CreatedPick object with the mapped data.
    """
    
    # Normalize to a proper UTC tzinfo (fixes compatibility with asyncpg/PostgreSQL)
    event_date = format_date(pick_data["event_date"])
    
    # Calculate parlay size from pick details
    parlay_size = len(pick_data.get("pick_details", []))
    
    created_pick = CreatedPick(
        created_pick_id=0,  # Will be set by database
        pick_id=pick_data["pick_id"],
        bet=pick_data["bet"],
        amount_won=pick_data["amount_won"],
        week_id=pick_data["week_id"],
        user_team_id=pick_data["user_team_id"],
        parlay_size=parlay_size,
        event_date=event_date
    )
    
    return created_pick

def map_to_created_pick_details(pick_details_data: List[dict], created_pick_id: int, event_date_str: str) -> List[CreatedPickDetail]:
    """Map a list of pick detail dictionaries to CreatedPickDetail objects.
    
    Parameters
    ----------
    pick_details_data : List[dict]
        List of data dictionaries containing pick detail information from RabbitMQ.
    created_pick_id : int
        The created_pick_id to associate with these details.
    event_date_str : str
        The event date string to be formatted.
    
    Returns
    -------
    List[CreatedPickDetail]
        A list of CreatedPickDetail objects with the mapped data.
    """
    
    # Normalize to a proper UTC tzinfo (fixes compatibility with asyncpg/PostgreSQL)
    event_date = format_date(event_date_str)
    
    created_pick_details = []
    
    for detail_data in pick_details_data:
        created_pick_detail = CreatedPickDetail(
            created_pick_detail_id=0,  # Will be set by database
            pick_detail_id=detail_data["pick_detail_id"],
            game_id=detail_data["game_id"],
            spread=float(detail_data["spread"]),
            total=float(detail_data["total"]),
            is_correct=detail_data["is_correct"],
            created_pick_id=created_pick_id,
            football_team_id=detail_data["football_team_id"],
            event_date=event_date
        )
        created_pick_details.append(created_pick_detail)
    
    return created_pick_details
