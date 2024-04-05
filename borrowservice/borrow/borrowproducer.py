import pika
import json
from django.conf import settings

def BookProducer(book):
    amqp_url = settings.RABBITMQ_URL
    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
    channel = connection.channel()
    channel.queue_declare(queue="borrow_queue")
    channel.basic_publish(
        exchange= "borrow_exchange",
        routing_key= "borrow_queue",
        body= json.dumps({"book_id":book}),
    )
    connection.close()