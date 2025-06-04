import aio_pika
import json
from datetime import datetime
from features.leagues.repository import add_created_league
from features.leagues.schemas import LeagueToBeCreated

async def process_message(message: aio_pika.abc.AbstractIncomingMessage, exchange_name: str):
    async with message.process():  # Auto-acknowledgment on success
        raw_body = message.body.decode()
        print(f"[RabbitMQ:{exchange_name}] Received: {raw_body}")

        try:
            data = json.loads(raw_body)

            if isinstance(data.get("event_date"), str):
                data["event_date"] = datetime.fromisoformat(data["event_date"])

            _id = await update_message_status(data, exchange_name)

            print(f"[RabbitMQ:{exchange_name}] Processed message with ID: {_id if 'id' in locals() else 'N/A'}")

        except Exception as e:
            print(f"[RabbitMQ:{exchange_name}] Failed to process message: {e}")

async def update_message_status(data, exchange_name: str):
    """Update the message status in the database or log it."""

    if exchange_name == "league_exchange":
        league = LeagueToBeCreated(**data)
        return await add_created_league(league)

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
        user_team = UserTeamToBeCreated(**data)
        return await add_created_user_team(user_team)

    elif exchange_name == "week_exchange":
        # Handle week exchange logic
        return 0
    
    return 0