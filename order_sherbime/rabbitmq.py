import pika
import json
import logging

logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "orders"

def get_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    return connection

def publish_order_created(order_data: dict):
    """Publish order created event"""
    try:
        connection = get_connection()
        channel = connection.channel()

        # Declare queue as durable=True (important for production)
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        message = json.dumps(order_data)

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # Makes message persistent
            )
        )

        connection.close()
        logging.info("📦 Order event published to RabbitMQ successfully")

    except Exception as e:
        logging.error(f"❌ Failed to publish order: {e}")
        # Don't fail the order creation just because notification failed
