import asyncpg
from core.database import get_db_config
from features.picks.schemas import CreatedPick, CreatedPickDetail
from typing import List

async def add_created_pick(pick: CreatedPick) -> int:
    """Add a pick to the created_picks table
    
    Parameters
    ----------
    pick : CreatedPick
        The pick object to be added to the database
    
    Returns
    -------
    int
        Returns the created_pick_id if successful, 0 if failed
    """
    
    config = get_db_config()
    
    try:
        conn = await asyncpg.connect(**config)
        
        query = """
            INSERT INTO created_picks (
                pick_id, bet, amount_won, week_id, 
                user_team_id, parlay_size, event_date
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7
            ) RETURNING created_pick_id;
        """
        
        row = await conn.fetchrow(
            query,
            pick.pick_id,
            pick.bet,
            pick.amount_won,
            pick.week_id,
            pick.user_team_id,
            pick.parlay_size,
            pick.event_date
        )
        
        await conn.close()
        
        return row["created_pick_id"] if row else 0
        
    except Exception as e:
        print(f"Error inserting pick: {e}")
        return 0

async def add_created_pick_detail(pick_detail: CreatedPickDetail) -> int:
    """Add a pick detail to the created_pick_details table
    
    Parameters
    ----------
    pick_detail : CreatedPickDetail
        The pick detail object to be added to the database
    
    Returns
    -------
    int
        Returns the created_pick_detail_id if successful, 0 if failed
    """
    
    config = get_db_config()
    
    try:
        conn = await asyncpg.connect(**config)
        
        query = """
            INSERT INTO created_pick_details (
                pick_detail_id, game_id, spread, total, 
                is_correct, created_pick_id, football_team_id, event_date
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8
            ) RETURNING created_pick_detail_id;
        """
        
        row = await conn.fetchrow(
            query,
            pick_detail.pick_detail_id,
            pick_detail.game_id,
            pick_detail.spread,
            pick_detail.total,
            pick_detail.is_correct,
            pick_detail.created_pick_id,
            pick_detail.football_team_id,
            pick_detail.event_date
        )
        
        await conn.close()
        
        return row["created_pick_detail_id"] if row else 0
        
    except Exception as e:
        print(f"Error inserting pick detail: {e}")
        return 0

async def delete_pick(pick_id: int, user_team_id: str) -> bool:
    """Delete a pick and its details from the created_picks and created_pick_details tables
    
    Parameters
    ----------
    pick_id : int
        The id of the pick to be deleted
    user_team_id : str
        The user team id associated with the pick
    
    Returns
    -------
    bool
        True if the deletion was successful, False otherwise
    """
    
    config = get_db_config()
    
    try:
        conn = await asyncpg.connect(**config)
        
        # Start a transaction to ensure both deletes succeed or fail together
        async with conn.transaction():
            # First delete pick details
            detail_result = await conn.execute(
                """DELETE FROM created_pick_details 
                   WHERE created_pick_id IN (
                       SELECT created_pick_id FROM created_picks 
                       WHERE pick_id = $1 AND user_team_id = $2
                   );""", 
                pick_id, user_team_id
            )
            
            # Then delete the pick
            pick_result = await conn.execute(
                "DELETE FROM created_picks WHERE pick_id = $1 AND user_team_id = $2;", 
                pick_id, user_team_id
            )
        
        await conn.close()
        
        return pick_result.startswith("DELETE") and pick_result.split()[1] != "0"
        
    except Exception as e:
        print(f"Error deleting pick: {e}")
        return False

async def get_picks_by_week(week_id: int) -> List[dict] | None:
    """Get all picks for a specific week
    
    Parameters
    ----------
    week_id : int
        The week id to retrieve picks for
    
    Returns
    -------
    List[dict] | None
        Returns a list of pick records if found, None otherwise
    """
    
    config = get_db_config()
    
    try:
        conn = await asyncpg.connect(**config)
        
        query = """
            SELECT created_pick_id, pick_id, bet, amount_won, 
                   week_id, user_team_id, parlay_size, event_date
            FROM created_picks 
            WHERE week_id = $1
            ORDER BY event_date DESC;
        """
        
        result = await conn.fetch(query, week_id)
        
        await conn.close()
        
        return [dict(row) for row in result] if result else None
        
    except Exception as e:
        print(f"An error occurred while reading picks for week {week_id}: {e}")
        return None

async def get_pick_by_id(pick_id: int) -> dict | None:
    """Get a pick by its id
    
    Parameters
    ----------
    pick_id : int
        The id of the pick to retrieve
    
    Returns
    -------
    dict | None
        Returns the pick record if found, None otherwise
    """
    
    config = get_db_config()
    
    try:
        conn = await asyncpg.connect(**config)
        
        query = """
            SELECT created_pick_id, pick_id, bet, amount_won, 
                   week_id, user_team_id, parlay_size, event_date
            FROM created_picks 
            WHERE pick_id = $1;
        """
        
        result = await conn.fetchrow(query, pick_id)
        
        await conn.close()
        
        return dict(result) if result else None
        
    except Exception as e:
        print(f"An error occurred while reading pick {pick_id}: {e}")
        return None

async def get_pick_details_by_pick_id(created_pick_id: int) -> List[dict] | None:
    """Get all pick details for a specific pick
    
    Parameters
    ----------
    created_pick_id : int
        The created pick id to retrieve details for
    
    Returns
    -------
    List[dict] | None
        Returns a list of pick detail records if found, None otherwise
    """
    
    config = get_db_config()
    
    try:
        conn = await asyncpg.connect(**config)
        
        query = """
            SELECT created_pick_detail_id, pick_detail_id, game_id, 
                   spread, total, is_correct, created_pick_id, 
                   football_team_id, event_date
            FROM created_pick_details 
            WHERE created_pick_id = $1
            ORDER BY pick_detail_id;
        """
        
        result = await conn.fetch(query, created_pick_id)
        
        await conn.close()
        
        return [dict(row) for row in result] if result else None
        
    except Exception as e:
        print(f"An error occurred while reading pick details for pick {created_pick_id}: {e}")
        return None
