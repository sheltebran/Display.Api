from features.leagues.schemas import LeagueToBeCreated, CreatedLeague
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

    created_league = CreatedLeague(created_league_id=0, league_id=league["league_id"], 
                                   name=league["name"], url=league["url"], 
                                   sport_id=league["sport_id"], event_date=league["event_date"])
    
    return created_league


