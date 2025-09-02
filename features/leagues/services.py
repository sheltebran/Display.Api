from core.enums import CreatedStatus
from features.leagues.mappings import map_to_created_league
from features.leagues.repository import (
    delete_league,
    add_created_league
)

async def process_league_message(data):
    """Process a league message and delete the league if necessary.

    Parameters
    ----------
    data : 
        Data that will be used to process the league message

    Returns
    -------
    CreatedLeague or None
        Returns a CreatedLeague object if the league is created successfully, or None if the league is deleted.
    """

    # Remove any entries like this one
    await delete_league(data["sport_id"], data["name"])
    
    try:
        if data["status"] == CreatedStatus.DELETE:
            # If the status is DELETE, return that processing is complete
            return True
        
        league = map_to_created_league(data)

        # Add the new message to the created_leagues table
        result = await add_created_league(league)

        return True if result > 0 else False

    except Exception as e:
        print(f"Error adding league: {e}")
        return True
            
    
