import psycopg2
from core.database import get_db_config
from datetime import datetime
from datetime import timezone
from features.user_teams.schemas import UserTeamToBeCreated

async def add_created_user_team(user_team: UserTeamToBeCreated):
    """Add a user team to the created_user_teams table

    Returns
    -------
    new_id: int
        Returns an integer value. If the value is 0
        or less then the operation failed unless a delete operation was requested.
    """

    # Validate the user_team object
    if (user_team.status not in ["new", "update", "delete"]):
        raise ValueError(f"Invalid status: {user_team.status}. Must be one of 'new', 'update', or 'delete'.")

    config = get_db_config()
    
    with psycopg2.connect(**config) as conn:
        conn.autocommit = True
        cur = conn.cursor()

    # Ensure there is no existing entry for the user_team_id
    cur.execute("""DELETE FROM created_user_teams WHERE user_team_id = %s;""", (user_team.user_team_id))

    if (user_team.status == "delete"):
        # If the status is delete, we don't need to insert a new record
        conn.commit()
        cur.close()
        conn.close()
        return 1

    # Insert the new user team
    cur.execute(f"INSERT INTO created_user_teams ('user_team_id', 'name', 'starting_amount', 'is_paid', 'is_active', 'slogan', 'email', 'season_id', 'user_id', 'event_date') VALUES ({user_team.user_team_id}, {user_team.name}, {user_team.starting_amount}, {user_team.is_paid}, {user_team.is_active}, {user_team.slogan}, {user_team.email}, {user_team.season_id}, {user_team.event_date}, {datetime.now(timezone.utc)}) RETURNING created_user_team_id;")
    
    row = cur.fetchone()
    new_id = row[0] if row and isinstance(row[0], int) else 0

    conn.commit()
    cur.close()
    conn.close()

    return new_id