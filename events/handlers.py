# Event handlers or message consumers
import pika

def callback(ch, method, properties, body):
    print(f"Received message from {method.exchange}: {body}")

# Replace with your actual connection values
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_user = 'guest'
rabbitmq_password = 'guest'

# Set up credentials and connection parameters
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection_params = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=credentials
)

# Connect to RabbitMQ
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare the fanout exchanges
exchanges = ['league_exchange', 'user_team_exchange', 'week_exchange', 'pick_exchange', 'default_pick_exchange', 'ranking_exchange', 'results_exchange']
queues = []

for exchange in exchanges:
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key="#")
    queues.append(queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Declare the queue and bind it to the exchange
# channel.queue_declare(queue='league_for_displays', durable=True)
# channel.queue_bind(exchange='league_exchange', queue='league_for_displays')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# channel.basic_consume(
#     queue='league_for_displays', on_message_callback=callback, auto_ack=True)

# Start consuming
# try:
#     channel.start_consuming()
# except KeyboardInterrupt:
#     print("Interrupted")
#     channel.stop_consuming()

# connection.close()
