import pika
import json
import logging

logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = "rabbitmq"


def get_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    return connection


def publish_order_created(order_data: dict):
    """
    Publishes order created event to RabbitMQ
    """
    try:
        connection = get_connection()
        channel = connection.channel()

        channel.queue_declare(queue="orders")

        message = json.dumps(order_data)

        channel.basic_publish(
            exchange="",
            routing_key="orders",
            body=message
        )

        connection.close()

        logging.info("📦 Order event published to RabbitMQ")

    except Exception as e:
        logging.error(f"❌ Failed to publish order: {e}")
