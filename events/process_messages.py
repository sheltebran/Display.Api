import aio_pika
import json
from datetime import datetime
from core.enums import CreatedStatus
from features.leagues.mappings import map_to_created_league
from features.leagues.repository import add_created_league, delete_league
from features.leagues.schemas import LeagueToBeCreated
from features.user_teams.repository import add_created_user_team
from features.user_teams.schemas import UserTeamToBeCreated
from camel_converter import dict_to_snake


async def process_message(message: aio_pika.abc.AbstractIncomingMessage, exchange_name: str):
    async with message.process():  # Auto-acknowledgment on success
        raw_body = message.body.decode()
        print(f"[RabbitMQ:{exchange_name}] Received: {raw_body}")

        try:
            # Decode the message body and parse JSON
            json_data = json.loads(raw_body)
            snake_case_data = dict_to_snake(json_data)

            await delete_league(snake_case_data['league_id'])

            # Delete the league if the status is DELETE
            if snake_case_data["status"] == CreatedStatus.DELETE:
                print(f"[RabbitMQ:{exchange_name}] Message with status DELETE received, skipping processing.")
                return
            
            league = map_to_created_league(snake_case_data)

            # Process the message based on the exchange name
            _id = await update_message_status(league, exchange_name)

            # Log the processed message ID or raise an error if the ID is not valid
            if _id > 0:
                print(f"[RabbitMQ:{exchange_name}] Processed message with ID: {_id if 'id' in locals() else 'N/A'}")
            else:
                raise ValueError(f"[RabbitMQ:{exchange_name}] Update failed.")

        except Exception as e:
            print(f"[RabbitMQ:{exchange_name}] Failed to process message: {e}")

async def update_message_status(data, exchange_name: str):
    """Update the status of a message based on the exchange name.

    Parameters
    ----------
    data : Class
        Data that will be used to update the status of the message
    exchange_name : str
        Exchange name that will be used to determine the type of message

    Returns
    -------
    int
        Returns an integer value. If the value is 0 or less, the operation failed.
    """

    if exchange_name == "league_exchange":
        return await add_created_league(data)

    elif exchange_name == "default_pick_exchange":
        # Handle default pick exchange logic
        return 0

    elif exchange_name == "pick_exchange":
        # Handle pick exchange logic
        return 0

    elif exchange_name == "ranking_exchange":
        # Handle ranking exchange logic
        return 0

    elif exchange_name == "user_team_exchange":
        # Handle user team exchange logic
        # user_team = UserTeamToBeCreated(**data)
        # return await add_created_user_team(user_team)
        return 0

    elif exchange_name == "week_exchange":
        # Handle week exchange logic
        return 0
    
    return 0