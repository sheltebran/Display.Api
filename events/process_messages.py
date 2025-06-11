import aio_pika
import json
from features.leagues.services import process_league_message
from features.user_teams.repository import add_created_user_team
from features.user_teams.services import process_user_team_message
from camel_converter import dict_to_snake

async def process_message(message: aio_pika.abc.AbstractIncomingMessage, exchange_name: str):
    async with message.process():  # Auto-acknowledgment on success
        """Process a RabbitMQ message based on the exchange name."""

        raw_body = message.body.decode()
        print(f"[RabbitMQ:{exchange_name}] Received: {raw_body}")

        try:
            # Decode the message body and parse JSON
            json_data = json.loads(raw_body)
            snake_case_data = dict_to_snake(json_data)

            # Process the message based on the exchange name
            success = await update_message_status(snake_case_data, exchange_name)

            # Log the processed message ID or raise an error if the ID is not valid
            if success:
                print("[RabbitMQ:{exchange_name}] Processed message successfully")
            else:
                print(f"[RabbitMQ:{exchange_name}] Process failed.")

        except Exception as e:
            print(f"[RabbitMQ:{exchange_name}] Failed to process message: {e}")

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
        # Handle default pick exchange logic
        return -1

    elif exchange_name == "pick_exchange":
        # Handle pick exchange logic
        return -1

    elif exchange_name == "ranking_exchange":
        # Handle ranking exchange logic
        return -1

    elif exchange_name == "user_team_exchange":
        # Handle user team exchange logic
        user_team = await process_user_team_message(data)
        if user_team is not None:
            return await add_created_user_team(user_team) 
        else:
            return -1

    elif exchange_name == "week_exchange":
        # Handle week exchange logic
        return -1
    
    return 0

