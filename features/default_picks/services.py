from core.enums import CreatedStatus
from features.default_picks.mappings import map_to_created_default_pick
from features.default_picks.repository import add_created_default_pick, delete_default_pick

async def process_default_pick_message(data):
    """Process a default pick message and delete the default pick if necessary.

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
    await delete_default_pick(data["game_id"], data["week_id"])

    try:
        if data["status"] == CreatedStatus.DELETE:
            # If the status is DELETE, return that processing is complete
            return True
        
        default_pick = map_to_created_default_pick(data)

        # Add the new message to the created_default_picks table
        result = await add_created_default_pick(default_pick)

        return True if result > 0 else False

    except Exception as e:
        print(f"Error adding default pick: {e}")
        return False

