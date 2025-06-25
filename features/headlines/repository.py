import asyncpg
from core.database import get_db_config
from datetime import datetime
from features.headlines.models import Headline
from features.headlines.schemas import HeadlineCreate
from typing import Any

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

    try:
        conn = await asyncpg.connect(**config)

        pub_date = datetime.strptime(headline.pub_date, '%m/%d/%Y %H:%M:%S')

        query = """
            INSERT INTO headlines (
                heading, story, link, pub_date, league_id
            )
            VALUES (
                $1, $2, $3, $4, $5
            )
            RETURNING headline_id;
        """

        row = await conn.fetchrow(
            query,
            headline.heading,
            headline.story,
            headline.link,
            pub_date,
            headline.league_id
        )

    except Exception as e:
        print(f"Error inserting headline: {e}")
        return 0

    await conn.close()

    return row["headline_id"] if row else 0



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

    try:
        conn = await asyncpg.connect(**config)

        query = """
            SELECT headline_id, heading, story, link, pub_date, league_id
            FROM headlines
            WHERE league_id = $1
            ORDER BY pub_date LIMIT $2
        """

        rows = await conn.fetch(query, league_id, limit)

    except Exception as e:
        print(f"Error reading headlines: {e}")
        return 0
    
    await conn.close()

    return [Headline(*item) for item in headline_list]

