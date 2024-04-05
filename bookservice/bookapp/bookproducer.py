import pika
import json
from django.conf import settings


def BookProducer(book):
    amqp_url = settings.RABBITMQ_URL

# For Establishing connection with the RABBITMQ Server
    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
    channel = connection.channel()

    channel.queue_declare("borrow_book_queue")
# Publish method is for sending the message
    channel.basic_publish(
        exchange="book_exchange", routing_key="book_queue", body=json.dumps(book)
    )
    
    print(f"[x] Book request published: {book}")

    connection.close()
