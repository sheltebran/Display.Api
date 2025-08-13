import logging
from core.enums import CreatedStatus
from features.weeks.mappings import map_to_created_week
from features.weeks.repository import add_created_week, delete_week

async def process_week_message(data):
    """Process a week message and delete the week if necessary.

    Parameters
    ----------
    data : 
        Data that will be used to process the week message

    Returns
    -------
    CreatedWeek or None
        Returns a CreatedWeek object if the week is created successfully, or None if the week is deleted.
    """

    # Remove any entries like this one
    await delete_week(data["week_number"], data["season_id"])

    logger = logging.getLogger(__name__)

    try:
        if data["status"] == CreatedStatus.DELETE:
            # If the status is DELETE, return that processing is complete
            return True
        
        week = map_to_created_week(data)

        # Add the new message to the created_weeks table
        result = await add_created_week(week)

        return True if result > 0 else False

    except Exception as e:
        logger.exception(f"Error adding week: {e}")
        return False


