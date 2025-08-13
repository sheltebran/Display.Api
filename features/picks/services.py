import logging
from core.enums import CreatedStatus
from features.picks.mappings import map_to_created_pick, map_to_created_pick_details
from features.picks.repository import add_created_pick, add_created_pick_detail, delete_pick

async def process_pick_message(data: dict) -> bool:
    """Process a pick message and delete the pick if necessary.

    Parameters
    ----------
    data : dict
        Data that will be used to process the pick message

    Returns
    -------
    bool
        Returns True if the pick is processed successfully, False otherwise.
    """

    logger = logging.getLogger(__name__)

    try:
        # Remove any entries like this one (delete-first pattern)
        await delete_pick(data["pick_id"], data["user_team_id"])

        if data["status"] == CreatedStatus.DELETE:
            # If the status is DELETE, return that processing is complete
            return True

        # Map the pick data to a CreatedPick object
        pick = map_to_created_pick(data)

        # Add the new pick to the created_picks table
        created_pick_id = await add_created_pick(pick)

        if created_pick_id <= 0:
            logger.error(f"Failed to create pick with id {data['pick_id']}")
            return False

        # Process pick details if they exist
        pick_details_data = data.get("pick_details", [])
        if pick_details_data:
            # Map and add each pick detail
            pick_details = map_to_created_pick_details(
                pick_details_data,
                created_pick_id,
                data["event_date"]
            )

            # Add all pick details
            for pick_detail in pick_details:
                detail_result = await add_created_pick_detail(pick_detail)
                if detail_result <= 0:
                    logger.error(f"Failed to create pick detail with id {pick_detail.pick_detail_id}")
                    # Note: In a production system, you might want to rollback the pick creation
                    # or implement a more sophisticated error handling strategy

        return True

    except Exception as e:
        logger.exception(f"Error processing pick message: {e}")
        return False
