import asyncpg
from core.database import get_db_config
from features.user_teams.schemas import CreatedUserTeam

async def add_created_user_team(user_team: CreatedUserTeam):
    """Add a user team to the created_user_teams table

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
            INSERT INTO created_user_teams (
                user_team_id, name, starting_amount, is_paid, payment_reference,
                is_active, slogan, email, season_id, user_id, event_date
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11
            )
            RETURNING created_user_team_id;
        """

        row = await conn.fetchrow(
            query,
            str(user_team.user_team_id),
            user_team.name,
            user_team.starting_amount,
            user_team.is_paid,
            user_team.payment_reference,
            user_team.is_active,
            user_team.slogan,
            user_team.email,
            str(user_team.season_id),
            str(user_team.user_id),
            user_team.event_date
        )

        await conn.close()

        return row["created_user_team_id"] if row else 0

    except Exception as e:
        print(f"Error inserting user team: {e}")
        return 0
    

async def delete_user_team(user_team_id: str):
    """Delete a user team from the created_user_teams table

    Parameters
    ----------
    user_team_id : uuid for string
        The id of the user team to be deleted

    Returns
    -------
    bool
        True if the deletion was successful, False otherwise
    """
    
    config = get_db_config()

    try:
        conn = await asyncpg.connect(**config)

        result = await conn.execute(
            "DELETE FROM created_user_teams WHERE user_team_id = %s;", 
            user_team_id,
        )

        conn.close()

        return result.startswith("DELETE") and result.split()[1] != "0"
    
    except Exception as e:
        print(f"An error occurred while deleting user team {user_team_id}: {e}")
        return False
    
    
async def get_user_team(user_team_id: str):
    """Get user team by user_team_id

    Parameters
    ----------
    user_team_id : str
        The id of the user team to be retrieved

    Returns
    -------
    int

        A list of integer values indicating the id for each of the leagues
    """
    
    config = get_db_config()

    try:
        conn = await asyncpg.connect(**config)

        # Read the user team by user_team_id
        result = await conn.execute(
            "SELECT * FROM created_user_teams WHERE user_team_id = %s;", 
            user_team_id,
        )
        
        conn.close()

        return result if result else None

    except Exception as e:
            print(f"An error occurred while reading user team {user_team_id}: {e}")
            return False
 
