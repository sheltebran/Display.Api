from core.enums import CreatedStatus
from features.user_teams.mappings import map_to_created_user_team
from features.user_teams.repository import delete_user_team

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

    await delete_user_team(data["user_team_id"])

    if data["status"] == CreatedStatus.DELETE:
        # If the status is DELETE, return none
        return None
            
    return map_to_created_user_team(data)
