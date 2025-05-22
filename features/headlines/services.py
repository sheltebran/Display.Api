# Business logic
from core.database import get_connection
from features.headlines.models import Headline
from features.headlines.schemas import HeadlineCreate
from typing import List
from repository import add_headline, get_leagues

# Create new headlines
async def create_headlines(sport_id: int):
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

    leagues = await get_leagues(sport_id)

    result = True

    for league in leagues
        headline = HeadlineCreate("Test", "Test", "Test", "2024-10-10T00:00:00", league)
        row = await add_headline(headline)
        if row is None:
            result = False
            break

    return result

# Get all headlines listed in the database
async def get_all_headlines():
    """Get all headlines

    Function to extract all headlines in the database and send back
    to caller.

    Returns
    -------
    Headlines: List[tuple, Headlines]
        Tuple starting with string and followed by the Headline class.
    """
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT headline_id, headline_type, heading, story, link, pub_date
        FROM headlines ORDER BY pub_date
    """)
    
    headline_list = cur.fetchall()
    cur.close()
    conn.close()

    return headline_list

# Import data from sport news source
async def import_headlines(season_id: int):
    
