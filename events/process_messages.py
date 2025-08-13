import aio_pika
import json
import logging
from features.default_picks.services import process_default_pick_message
from features.leagues.services import process_league_message
from features.picks.services import process_pick_message
from features.user_teams.services import process_user_team_message
from features.weeks.services import process_week_message
from camel_converter import dict_to_snake

async def process_message(message: aio_pika.abc.AbstractIncomingMessage, exchange_name: str):
    async with message.process():  # Auto-acknowledgment on success
        """Process a RabbitMQ message based on the exchange name."""

        raw_body = message.body.decode()
        logger = logging.getLogger(__name__)
        logger.info(f"[RabbitMQ:{exchange_name}] Received: {raw_body}")

        try:
            # Decode the message body and parse JSON
            json_data = json.loads(raw_body)
            snake_case_data = dict_to_snake(json_data)

            # Process the message based on the exchange name
            success = await update_message_status(snake_case_data, exchange_name)

            # Log the processed message ID or raise an error if the ID is not valid
            if success:
                logger.info("[RabbitMQ:{exchange_name}] Processed message successfully")
            else:
                logger.error(f"[RabbitMQ:{exchange_name}] Process failed.")

        except Exception as e:
            logger.error(f"[RabbitMQ:{exchange_name}] Failed to process message: {e}")

async def update_message_status(data, exchange_name: str) -> int:
    """Update the status of a message based on the exchange name.

    Parameters
    ----------
    data : tuple or dict
        Data that will be used to update the status of the message
    exchange_name : str
        Exchange name that will be used to determine the type of message

    Returns
    -------
    bool
        Returns True if the message was processed successfully, False otherwise
    """

    if exchange_name == "league_exchange":
        result = await process_league_message(data)
        return result

    elif exchange_name == "default_pick_exchange":
        result = await process_default_pick_message(data)
        return result

    elif exchange_name == "pick_exchange":
        result = await process_pick_message(data)
        return result

    elif exchange_name == "ranking_exchange":
        # Handle ranking exchange logic
        return -1

    elif exchange_name == "user_team_exchange":
        result = await process_user_team_message(data)
        return result

    elif exchange_name == "week_exchange":
        result = await process_week_message(data)
        return result
    
    return False

