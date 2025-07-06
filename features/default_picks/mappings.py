from core.date_helpers import format_date
from features.default_picks.schemas import CreatedDefaultPick

def map_to_created_default_pick(default_pick):
    """Map a default pick dictionary to a CreatedDefaultPick object.

    Parameters
    ----------
    default_pick : Dict[Any, Any]
        Data dictionary containing default pick information.

    Returns
    -------
    CreatedDefaultPick
        A CreatedDefaultPick object with the mapped data.
    """
    
    # Normalize to a proper UTC tzinfo (fixes compatibility with asyncpg/PostgreSQL)
    event_date = format_date(default_pick["event_date"])

    created_default_pick = CreatedDefaultPick(
        created_default_pick_id=0,
        bet=default_pick["bet"],
        game_id=default_pick["game_id"],
        favorite_team_id=default_pick["favorite_team_id"],
        favorite_team_name=default_pick["favorite_team_name"],
        spread=default_pick["spread"],
        week_id=default_pick["week_id"],
        week_number=default_pick["week_number"],
        event_date=event_date
    )

    return created_default_pick

