from fastapi import FastAPI
import asyncio
import aio_pika
from events.process_messages import process_message

app = FastAPI()

RABBITMQ_URL = "amqp://guest:guest@localhost/"

# Define your exchange/queue bindings here
BINDINGS = [
    {"exchange": "default_pick_exchange", "queue": "default_pick_for_displays"},
    {"exchange": "league_exchange", "queue": "league_for_displays"},
    {"exchange": "pick_exchange", "queue": "pick_for_displays"},
    {"exchange": "ranking_exchange", "queue": "ranking_for_displays"},
    {"exchange": "user_team_exchange", "queue": "user_team_for_displays"},
    {"exchange": "week_exchange", "queue": "week_for_displays"}
]

async def setup_binding(channel, exchange_name, queue_name):
    exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.FANOUT, durable=True)
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange)

    # Define a wrapper that passes exchange_name to process_message
    async def wrapped_process_message(message: aio_pika.abc.AbstractIncomingMessage):
        await process_message(message, exchange_name)

    print(f"[RabbitMQ] Bound queue '{queue_name}' to exchange '{exchange_name}'")
    await queue.consume(wrapped_process_message)

async def rabbitmq_listener():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    for binding in BINDINGS:
        await setup_binding(channel, binding["exchange"], binding["queue"])

