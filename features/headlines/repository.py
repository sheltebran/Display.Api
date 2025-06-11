# DB access layer
import psycopg2
from core.database import get_db_config
from datetime import datetime
from features.headlines.models import Headline
from features.headlines.schemas import HeadlineCreate
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
    
    config = get_db_config()
    
    with psycopg2.connect(**config) as conn:
        conn.autocommit = True
        cur = conn.cursor()

    pub_date = datetime.strptime(headline.pub_date, '%m/%d/%Y %H:%M:%S')

    cur.execute(f"INSERT INTO headlines (heading, story, link, pub_date, league_id) VALUES ('{headline.heading}', '{headline.story}', '{headline.link}', '{pub_date}', {headline.league_id}) RETURNING headline_id;")
    
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
    config = get_db_config()
    
    with psycopg2.connect(**config) as conn:
        conn.autocommit = True
        cur = conn.cursor()
    
    cur.execute(f"SELECT headline_id, heading, story, link, pub_date, league_id FROM headlines WHERE league_id = {league_id} ORDER BY pub_date LIMIT {limit}")
    
    headline_list = cur.fetchall()
    cur.close()
    conn.close()

    return [Headline(*item) for item in headline_list]

