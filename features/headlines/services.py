# Business logic
from core.database import get_connection
from features.headlines.schemas import HeadlineCreate, Headline
from typing import List
from repository import add_headline

# Create new headlines
async def create_headlines(season_id: int):
    """Request to get and create new headlines

    This function accesses a sports headlines feed, parses the data
    and stores the result in a database, removing the old content.

    Parameters
    ----------
    season_id : int
        Id for the season and for accessing the different leagues and urls
        for the sports feed.

    Returns
    -------
    Result: bool
        A true setting indicates the creation was successful.
    """    

    headline = HeadlineCreate(1, "Test", "Test", "Test", "2024-10-10T00:00:00")

    id = await add_headline(headline)

    return id

# Get all headlines listed in the database
def get_all_headlines():
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
def import_headlines(season_id: int):
    
