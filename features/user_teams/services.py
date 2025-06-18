from core.enums import CreatedStatus
from features.user_teams.mappings import map_to_created_user_team
from features.user_teams.repository import add_created_user_team, delete_user_team

async def process_user_team_message(data):
    """Process a user team message and delete the user team if necessary.

    Parameters
    ----------
    data : 
        Data that will be used to process the user team message

    Returns
    -------
    CreatedUserTeam or None
        Returns a CreatedUserTeam object if the user team is created successfully, or None if the user team is deleted.
    """

    # Remove any entries like this one
    await delete_user_team(data["name"], data["season_id"])

    try:
        if data["status"] == CreatedStatus.DELETE:
            # If the status is DELETE, return that processing is complete
            return True
        
        user_team = map_to_created_user_team(data)

        # Add the new message to the created_user_teams table
        result = await add_created_user_team(user_team)

        return True if result > 0 else False

    except Exception as e:
        print(f"Error adding user team: {e}")
        return False


