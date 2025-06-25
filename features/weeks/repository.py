import asyncpg
from core.database import get_db_config
from features.weeks.schemas import CreatedWeek

async def add_created_week(week: CreatedWeek):
    """Add a week to the created_weeks table

    Returns
    -------
    new_id: int
        Returns an integer value. If the value is 0
        or less then the operation failed
    """
    
    config = get_db_config()
    
    try:
        conn = await asyncpg.connect(**config)

        query = """
            INSERT INTO created_weeks (
                week_id, week_number, start_date, end_date, deadline_date,
                season_id, event_date
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7
            )
            RETURNING created_week_id;
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

        return row["created_week_id"] if row else 0

    except Exception as e:
        print(f"Error inserting week: {e}")
        return 0  

async def delete_week(week_number: int, season_id: str):
    """Delete a week from the created_weeks table

    Parameters
    ----------
    week_number : int
        The number of the week to be deleted
    season_id : str
        The id of the season to which the week belongs

    Returns
    -------
    bool
        True if the deletion was successful, False otherwise
    """
    
    config = get_db_config()
    
    conn = await asyncpg.connect(**config)

    result = await conn.execute(
        "DELETE FROM created_weeks WHERE week_number = $1 AND season_id = $2;", week_number, season_id
    )

    await conn.close()

    return result.startswith("DELETE") and result.split()[1] != "0"
      
async def get_week(week_id: str):
    """Get week by week_id

    Parameters
    ----------
    week_id : str
        The id of the week to be retrieved

    Returns
    -------
    CreatedWeek | None
        Returns a CreatedWeek object if found, None otherwise
    """
    
    config = get_db_config()

    try:
        conn = await asyncpg.connect(**config)

        # Read the week by week_id
        result = await conn.execute(
            "SELECT * FROM created_weeks WHERE week_id = $1;", 
            week_id,
        )
        
        conn.close()

        return result if result else None

    except Exception as e:
            print(f"An error occurred while reading week {week_id}: {e}")
            return False
 
