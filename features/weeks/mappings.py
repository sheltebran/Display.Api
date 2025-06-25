from core.date_helpers import format_date
from features.weeks.schemas import CreatedWeek

def map_to_created_week(week):
    """Map a week dictionary to a CreatedWeek object.

    Parameters
    ----------
    week : Dict[Any, Any]
        Data dictionary containing week information.

    Returns
    -------
    CreatedWeek
        A CreatedWeek object with the mapped data.
    """
    
    # Normalize to a proper UTC tzinfo (fixes compatibility with asyncpg/PostgreSQL)
    event_date = format_date(week["event_date"])

    created_week = CreatedWeek(
        created_user_team_id=0,
        week_id=week["week_id"],
        week_number=week["week_number"],
        start_date=week["start_date"],
        end_date=week["end_date"],
        deadline_date=week["deadline_date"],
        season_id=week["season_id"],
        event_date=event_date
    )

    return created_week

