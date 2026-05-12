import pika
import json
import time
import os
import logging
import socket

logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "order_created"


def wait_for_rabbitmq(host, port=5672, timeout=60):
    logging.info("⏳ Waiting for RabbitMQ to be ready...")

    start = time.time()

    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                logging.info("✅ RabbitMQ is reachable!")
                return
        except OSError:
            if time.time() - start > timeout:
                raise Exception("RabbitMQ did not become ready in time")

            time.sleep(2)


def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())

        logging.info("=================================")
        logging.info("📦 NEW ORDER RECEIVED")
        logging.info(message)
        logging.info("📨 Sending notification...")
        logging.info("=================================")

    except Exception as e:
        logging.error(f"Error processing message: {e}")


def consume_messages():
    while True:
        try:
            wait_for_rabbitmq(RABBITMQ_HOST)

            logging.info(f"🔌 Connecting to RabbitMQ at {RABBITMQ_HOST}...")

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )

            channel = connection.channel()

            # Ensure queue exists (safe even if deleted manually)
            channel.queue_declare(queue=QUEUE_NAME, durable=True)

            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback,
                auto_ack=True
            )

            logging.info("👂 Waiting for messages...")
            channel.start_consuming()

        except Exception as e:
            logging.error(f"❌ Consumer crashed: {e}")
            time.sleep(5)
