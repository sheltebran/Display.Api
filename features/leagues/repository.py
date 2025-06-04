import psycopg2
from core.database import get_db_config
from datetime import datetime
from datetime import timezone
from features.leagues.schemas import LeagueToBeCreated

async def get_league_ids(sport_id: int):
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
    config = get_db_config()
    
    with psycopg2.connect(**config) as conn:
        conn.autocommit = True
        cur = conn.cursor()

    # Read the list of leagues ids
    cur.execute(f"SELECT league_id FROM created_leagues WHERE sport_id={sport_id}")

    # Fetch all rows from the executed query extracting the league id
    league_ids = [r[0] for r in cur.fetchall() if isinstance(r[0], int)]

    conn.commit()
    cur.close()
    conn.close()

    return league_ids

async def add_created_league(league: LeagueToBeCreated):
    """Add a league to the created_leagues table

    Returns
    -------
    new_id: int
        Returns an integer value. If the value is 0
        or less then the operation failed
    """

    # Validate the league object
    if (league).status not in ["new", "update", "delete"]):
        raise ValueError(f"Invalid status: {user_team.status}. Must be one of 'new', 'update', or 'delete'.")
    
    config = get_db_config()
    
    with psycopg2.connect(**config) as conn:
        conn.autocommit = True
        cur = conn.cursor()

    # Ensure there is no existing entry for the league_id
    cur.execute("""DELETE FROM created_leagues WHERE league_id = %s;""", (league.league_id))

    if (league.status == "delete"):
        # If the status is delete, we don't need to insert a new record
        conn.commit()
        cur.close()
        conn.close()
        return 1

    cur.execute(f"INSERT INTO created_leagues ('league_id', 'name', 'url', 'sport_id', 'event_date') VALUES ({league.league_id, league.name, league.url, league.sport_id, datetime.now(timezone.utc)}) RETURNING created_league_id;")
    
    row = cur.fetchone()
    new_id = row[0] if row and isinstance(row[0], int) else 0

    conn.commit()
    cur.close()
    conn.close()

    return new_id