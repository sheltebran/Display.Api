import asyncpg
from core.database import get_db_config
from features.leagues.schemas import CreatedLeague

async def add_created_league(league: CreatedLeague):
    """Add a league to the created_leagues table

    Returns
    -------
    row: int
        Returns an integer value. If the value is 0
        or less then the operation failed
    """
    
    config = get_db_config()
    
    conn = await asyncpg.connect(**config)

    query = """
        INSERT INTO created_leagues (league_id, name, url, sport_id, event_date
        ) VALUES (
            $1, $2, $3, $4, $5
        ) RETURNING created_league_id;
    """

    row = await conn.fetchrow(
        query,
        league.league_id,
        league.name,
        league.url,
        league.sport_id,
        league.event_date
    )

    await conn.close()

    return row["created_league_id"] if row else 0

async def delete_league(sport_id: int, name: str):
    """Delete a league from the created_leagues table

    Parameters
    ----------
    sport_id: int
        The sport id of the league
    name : str
        THe name of the league

    Returns
    -------
    bool
        Returns True if the deletion was successful, False otherwise
    """
    
    config = get_db_config()
    
    conn = await asyncpg.connect(**config)

    result = await conn.execute(
        "DELETE FROM created_leagues WHERE sport_id = $1 AND name = $2;", sport_id, name
    )

    await conn.close()

    return result.startswith("DELETE") and result.split()[1] != "0"

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
    
    try:
        config = get_db_config()

        conn = await asyncpg.connect(**config)

        # Read the league ids by sport_id
        result = await conn.fetch(
            "SELECT league_id, url FROM created_leagues WHERE sport_id = $1;", sport_id,
        )
        
        await conn.close()

        return result if result else None

    except Exception as e:
            print(f"An error occurred while reading leagues in sport {sport_id}: {e}")
            return False

async def get_league_by_id(league_id: int):
    """Read a league by its id

    Parameters
    ----------
    league_id : int
        The id of the league to read

    Returns
    -------
    result : str or None
        Returns the league information if found, otherwise None
    """

    try:
        config = get_db_config()

        conn = await asyncpg.connect(**config)

        query = """
            SELECT league_id, url FROM created_leagues WHERE league_id = $1;
        """

        # Obtain the league information
        result = await conn.fetchone(query, league_id)

        await conn.close()

        return result if result else None

    except Exception as e:
        print(f"An error occurred while reading league {league_id}: {e}")
        return None

