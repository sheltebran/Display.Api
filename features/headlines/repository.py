# DB access layer
from core.database import get_connection
from features.headlines.models import Headline
from features.headlines.schemas import HeadlineCreate
from datetime import datetime
from typing import Any, List

async def add_headline(headline: HeadlineCreate):
    """Add new headline

    Add a new headline and return the result of the addition

    Returns
    -------
    new_id: int
        Returns an integer value. If the value is 0
        or less then the operation failed
    """
    conn = get_connection()

    cur = conn.cursor()

    HEADLINE_INSERT = f"INSERT INTO headlines (headline_type, heading, story, link, pub_date) VALUES ({headline.heading}, {headline.story}, {headline.link}, {datetime.strptime(headline.pub_date, '%m/%d/%y %H:%M:%S'), headline.league_id});RETURNING headline_id;"

    cur.execute(HEADLINE_INSERT)
    
    row: tuple[Any, ...] | None = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return row

async def get_all_headlines(league_id: int, limit: int):
    """Get all headlines for a league returning no more than the limit set

    Parameters
    ----------
    league_id : int
        Only retrieve headlines for this league
    limit : int
        Limit the number of lines extracted

    Returns
    -------
    List of Headlines
        Return a list of headlines for that league
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(f"SELECT headline_id, heading, story, link, pub_date, league_id FROM headlines WHERE league_id = {league_id} ORDER BY pub_date LIMIT {limit}")
    
    headline_list = cur.fetchall()
    cur.close()
    conn.close()

    return [Headline(*item) for item in headline_list]

async def get_leagues(sport_id: int):
    """Get all leagues for a sport

    Parameters
    ----------
    sport_id : int
        The sports id that will be used to acquire all leagues

    Returns
    -------
    List[int]
        A list of integer values indicating the id for each of the leagues
    """
    conn = get_connection()

    cur = conn.cursor()

    GET_LEAGUES=f"SELECT league_id FROM LEAGUES WHERE sport_id={sport_id}"

    cur.execute(GET_LEAGUES)

    # Read the list of leagues ids
    rows = cur.fetchall()
    leagues = [row[0] for row in rows if isinstance(row[0], int)]

    conn.commit()
    cur.close()
    conn.close()

    return leagues
