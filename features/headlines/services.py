# Business logic
from features.headlines.repository import add_headline, get_all_headlines
from features.leagues.repository import get_league_ids
from features.headlines.schemas import HeadlineCreate
from typing import List

# Create new headlines
async def create_sport_headlines(sport_id: int):
    """Request to get and create new headlines

    This function accesses a sports headlines feed, parses the data
    and stores the result in a database, removing the old content.

    Parameters
    ----------
    sport_id : int
        Id for the sport and for accessing the different leagues and urls
        for the sports feed.

    Returns
    -------
    Result: bool
        A true setting indicates the creation was successful.
    """    

    league_ids = await get_league_ids(sport_id)

    if not league_ids:
        return False
    
    result = True

    for league_id in league_ids:
        headline = HeadlineCreate("Test", "Test", "Test", "05/22/2025 00:00:00", league_id)
        row = await add_headline(headline)
        if row is None:
            result = False
            break

    return result

# Get all headlines listed in the database
async def get_headlines_by_league(league_id: int):
    """Get all headlines

    Function to extract all headlines in the database for a league and send back
    to caller.

    Returns
    -------
    Headlines: List[tuple, Headlines]
        Tuple starting with string and followed by the Headline class.
    """
    
    headlines = await get_all_headlines(league_id, 10)

    return headlines
    

# Import data from sport news source
# async def import_headlines(season_id: int):
    
