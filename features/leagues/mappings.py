from datetime import timezone
from dateutil.parser import parse
from features.leagues.schemas import CreatedLeague
from typing import List

def map_to_created_league(league):
    """Map a league dictionary to a CreatedLeague object.

    Parameters
    ----------
    league : Dict[Any, Any]
        Data dictionary containing league information.

    Returns
    -------
    CreatedLeague
        A CreatedLeague object with the mapped data.
    """

    event_date_str = league["event_date"]

    # Ensure it's timezone-aware
    event_date = parse(event_date_str)

    # Normalize to a proper UTC tzinfo (fixes compatibility with asyncpg/PostgreSQL)
    event_date = event_date.astimezone(timezone.utc)
        
    # Ensure it's timezone-aware
    # if event_date.tzinfo is None:
    #     event_date = event_date.replace(tzinfo=timezone.utc)

    created_league = CreatedLeague(
        created_league_id=0, 
        league_id=league["league_id"], 
        name=league["name"],
        url=league["url"], 
        sport_id=league["sport_id"],
        event_date=event_date
    )
    
    return created_league


