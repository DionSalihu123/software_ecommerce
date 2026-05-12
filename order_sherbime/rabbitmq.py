import json
import pika


RABBITMQ_HOST = "rabbitmq"


def publish_order_created(order_data):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    channel = connection.channel()

    # create queue if not exists
    channel.queue_declare(queue="order_created")

    # publish message
    channel.basic_publish(
        exchange="",
        routing_key="order_created",
        body=json.dumps(order_data)
    )

    print("Order event published")

    connection.close()
