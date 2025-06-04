from fastapi import FastAPI
import asyncio
import aio_pika
import json
from datetime import datetime
from features.leagues.repository import add_created_league
from features.leagues.schemas import CreatedLeague

app = FastAPI()

RABBITMQ_URL = "amqp://guest:guest@localhost/"  # change as needed
EXCHANGE_NAME = "league_exchange"
QUEUE_NAME = "display_queue"

async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    raw_body = message.body.decode()
    print(f"[RabbitMQ] Received: {raw_body}")

    # Step 1: Parse JSON string into a Python dict
    data = json.loads(raw_body)

    # Step 2: Convert event_date string to a datetime object (if needed)
    if isinstance(data.get("event_date"), str):
        data["event_date"] = datetime.fromisoformat(data["event_date"])

    # Step 3: Create a CreatedLeague object
    league = CreatedLeague(**data)

    # Step 4: Pass to your repository
    await add_created_league(league)

async def rabbitmq_listener():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    # Declare exchange and queue
    exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT, durable=True)
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.bind(exchange)

    print(f"[RabbitMQ] Listening on queue '{QUEUE_NAME}'...")

    # Start consuming
    await queue.consume(process_message)