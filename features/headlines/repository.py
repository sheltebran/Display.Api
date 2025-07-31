import asyncpg
from core.database import get_db_config
from datetime import datetime
from fastapi import HTTPException
from features.headlines.models import HeadlineDto
from typing import List

async def add_headline(headline, league_id: int):
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

        # Parse the publication date from the headline
        pub_date = datetime.strptime(headline.get("pubDate"), '%a, %d %b %Y %H:%M:%S %z')

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
            headline.get("title"),
            headline.get("description"),
            headline.get("link"),
            pub_date,
            league_id
        )

        await conn.close()

        return row["headline_id"] if row else 0

    except Exception as e:
        print(f"Error inserting headline: {e}")
        return 0


async def delete_headlines_for_league(league_id: int):
    """Delete all headlines for a specific league

    Parameters
    ----------
    league_id: int
        The ID of the league to delete headlines for

    Returns
    -------
    bool
        Returns True if the deletion was successful, False otherwise
    """

    config = get_db_config()

    conn = await asyncpg.connect(**config)

    result = await conn.execute(
        "DELETE FROM headlines WHERE league_id = $1;", league_id
    )

    await conn.close()

    return result.startswith("DELETE") and result.split()[1] != "0"


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
            SELECT heading, story, link, pub_date, league_id
            FROM headlines
            WHERE league_id = $1
            ORDER BY pub_date LIMIT $2
        """

        rows = await conn.fetch(query, league_id, limit)

        await conn.close()

        return [HeadlineDto(*item) for item in rows] if rows else []

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while writing {e}.")
    
