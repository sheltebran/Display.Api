from features.user_teams.schemas import CreatedUserTeam
from typing import List

def map_to_created_user_team(user_team):
    """Map a user team dictionary to a CreatedUserTeam object.

    Parameters
    ----------
    user_team : Dict[Any, Any]
        Data dictionary containing user team information.

    Returns
    -------
    CreatedUserTeam
        A CreatedUserTeam object with the mapped data.
    """

    created_user_team = CreatedUserTeam(
        created_user_team_id=0, 
        user_team_id=user_team["user_team_id"], 
        name=user_team["name"], 
        starting_amount=user_team["starting_amount"], 
        is_paid=user_team["is_paid"], 
        payment_reference=user_team["payment_reference"],
        is_active=user_team["is_active"],
        slogan=user_team["slogan"],
        email=user_team["email"],
        season_id=user_team["season_id"],
        user_id=user_team["user_id"],
        event_date=user_team["event_date"])
    
    return created_user_team

