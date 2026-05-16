import pika
import json
import logging
import time
import os
import socket
import httpx
from datetime import datetime

logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "orders"
USER_SERVICE_URL = "http://user-service:8000"


def get_user_email(user_id: int) -> str:
    """Fetch real user email from User Service"""
    try:
        response = httpx.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=5.0)
        if response.status_code == 200:
            user = response.json()
            return user.get("email", f"user{user_id}@example.com")
        logging.warning(f"Could not fetch user {user_id}, using fallback")
        return f"user{user_id}@example.com"
    except Exception as e:
        logging.warning(f"User service unavailable: {e}")
        return f"user{user_id}@example.com"


def print_order_notification(order_data: dict):
    """Beautiful console notification with real user email"""
    user_email = get_user_email(order_data.get('user_id'))

    print("\n" + "=" * 80)
    print("🎉 ORDER CONFIRMATION NOTIFICATION".center(80))
    print("=" * 80)
    print(f"📧 Sent To      : {user_email}")
    print(f"🆔 Order ID     : #{order_data.get('order_id')}")
    print(f"📅 Date         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🛒 Product ID   : {order_data.get('product_id')}")
    print(f"💰 Total Amount : ${float(order_data.get('total_amount', 0)):.2f}")
    print(f"🔑 License Key  : {order_data.get('license_key')}")
    print(f"📊 Status       : {order_data.get('status', 'pending').upper()}")
    print("-" * 80)
    print("✅ Notification processed successfully (Console Mode)")
    print("=" * 80 + "\n")


def callback(ch, method, properties, body):
    try:
        order_data = json.loads(body.decode())
        logging.info(f"📦 Received order #{order_data.get('order_id')} for notification")

        print_order_notification(order_data)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"❌ Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def wait_for_rabbitmq(host, port=5672, timeout=60):
    logging.info("⏳ Waiting for RabbitMQ to be ready...")
    start = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                logging.info("✅ RabbitMQ is reachable!")
                return True
        except OSError:
            if time.time() - start > timeout:
                logging.error("❌ RabbitMQ did not become ready in time")
                return False
            time.sleep(3)


def consume_messages():
    while True:
        try:
            if not wait_for_rabbitmq(RABBITMQ_HOST):
                time.sleep(5)
                continue

            logging.info(f"🔌 Connecting to RabbitMQ at {RABBITMQ_HOST}...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            channel = connection.channel()

            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback,
                auto_ack=False
            )

            logging.info("👂 Notification consumer is ready and waiting for orders...")
            channel.start_consuming()

        except Exception as e:
            logging.error(f"Consumer crashed: {e}. Restarting in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    consume_messages()
