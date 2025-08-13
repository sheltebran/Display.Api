import asyncpg
import logging
from core.database import get_db_config
from features.default_picks.schemas import CreatedDefaultPick

async def add_created_default_pick(week: CreatedDefaultPick):
    """Add a default pick to the created_default_picks table

    Returns
    -------
    new_id: int
        Returns an integer value. If the value is 0
        or less then the operation failed
    """
    
    logger = logging.getLogger(__name__)

    try:
        config = get_db_config()
    
        conn = await asyncpg.connect(**config)

        query = """
            INSERT INTO created_default_picks (
                game_id, bet, favorite_team_id,
                favorite_team_name, spread, week_id,
                week_number, event_date
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8
            )
            RETURNING created_default_pick_id;
        """

        row = await conn.fetchrow(
            query,
            week.week_id,
            week.week_number,
            week.start_date,
            week.end_date,
            week.deadline_date,
            week.season_id,
            week.event_date
        )

        await conn.close()

        return row["created_default_pick_id"] if row else 0

    except Exception as e:
        logger.exception(f"Error inserting default pick: {e}")
        return 0

async def delete_default_pick(game_id: int, week_id: int):
    """Delete a default pick from the created_default_picks table

    Parameters
    ----------
    game_id : int
        The id of the game associated with the default pick to be deleted
    week_id : int
        The id of the week associated with the default pick to be deleted

    Returns
    -------
    bool
        True if the deletion was successful, False otherwise
    """
    
    config = get_db_config()
    
    conn = await asyncpg.connect(**config)

    result = await conn.execute(
        "DELETE FROM created_default_picks WHERE game_id = $1 AND week_id = $2;", game_id, week_id
    )

    await conn.close()

    return result.startswith("DELETE") and result.split()[1] != "0"

async def get_default_pick(week_id: int):
    """Get default pick by week_id

    Parameters
    ----------
    week_id : int
        The id of the week to be retrieved

    Returns
    -------
    CreatedDefaultPick | None
        Returns a CreatedDefaultPick object if found, None otherwise
    """
    
    logger = logging.getLogger(__name__)

    try:
        config = get_db_config()

        conn = await asyncpg.connect(**config)

        # Read the week by week_id
        result = await conn.execute(
            "SELECT * FROM created_default_picks WHERE week_id = $1;", week_id,
        )
        
        conn.close()

        return result if result else None

    except Exception as e:
        logger.exception(f"An error occurred while reading default pick for week with id {week_id}: {e}")
        return False
 
