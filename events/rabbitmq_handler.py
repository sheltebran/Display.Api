import aio_pika
import logging
from fastapi import FastAPI

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
    """Setup a binding between an exchange and a queue.

    Parameters
    ----------
    channel : AbstractChannel
        The channel to use for the binding
    exchange_name : str
        The name of the exchange to bind
    queue_name : str
        The name of the queue to bind
        
    """

    exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.FANOUT, durable=True)
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange)

    # Define a wrapper that passes exchange_name to process_message
    async def wrapped_process_message(message: aio_pika.abc.AbstractIncomingMessage):
        await process_message(message, exchange_name)

    logger = logging.getLogger(__name__)
    logger.info(f"Bound queue '{queue_name}' to exchange '{exchange_name}'")
    
    await queue.consume(wrapped_process_message)

async def rabbitmq_listener():
    """Connect to RabbitMQ and start consuming messages.
    
    This function is called by the FastAPI lifespan context manager
    and is responsible for connecting to RabbitMQ and starting the
    consumer. The consumer will run until the application is stopped.
    
    """

    bindings = BINDINGS.copy()

    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    for binding in bindings:
        await setup_binding(channel, binding["exchange"], binding["queue"])

