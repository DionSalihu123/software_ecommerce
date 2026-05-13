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
QUEUE_NAME = "orders"          # Must match Order Service

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

def send_order_notification(order_data: dict):
    """Send notification (console + future email)"""
    try:
        logging.info("📧 Sending Order Confirmation Notification")
        logging.info(f"Order ID: {order_data.get('order_id')}")
        logging.info(f"User ID: {order_data.get('user_id')}")
        logging.info(f"Product ID: {order_data.get('product_id')}")
        logging.info(f"Total Amount: ${order_data.get('total_amount', 0):.2f}")

        # TODO: Later - Send real email here
        # For now, beautiful console log
        print("\n" + "="*60)
        print("🎉 ORDER CONFIRMATION EMAIL SENT (SIMULATED)")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Order #{order_data.get('order_id')}")
        print(f"Customer ID: {order_data.get('user_id')}")
        print(f"Product ID: {order_data.get('product_id')}")
        print(f"Amount: ${order_data.get('total_amount', 0):.2f}")
        print("Status: Order Received & Processing")
        print("="*60 + "\n")

    except Exception as e:
        logging.error(f"Failed to send notification: {e}")

def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())
        logging.info("📦 Received new order event!")

        send_order_notification(message)

        # Acknowledge message (safe)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        # Reject and requeue on error (optional)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

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

            channel.basic_qos(prefetch_count=1)  # Fair dispatch

            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback,
                auto_ack=False
            )

            logging.info(f"👂 Notification consumer started. Waiting for messages on queue: {QUEUE_NAME}")
            channel.start_consuming()

        except Exception as e:
            logging.error(f"Consumer crashed: {e}. Restarting in 5 seconds...")
            time.sleep(5)
