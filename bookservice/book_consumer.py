import os
import sys
import pika
import django
import json
from django.conf import settings
from sys import path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import sys

sys.path.append(str(BASE_DIR/"bookservice"))

path.append(BASE_DIR/"bookservice/settings.py")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookservice.settings")
django.setup()

from bookapp.models import book
from django.shortcuts import get_object_or_404

RABBITMQ_URL = settings.RABBITMQ_URL
print(RABBITMQ_URL)
params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(params)
channel = connection.channel()

def declare_queue(exchange_name ,queue_name):
    channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")
    channel.queue_declare(queue= queue_name)
    channel.queue_bind(exchange=exchange_name,queue=queue_name)

def borrow_consumer(channel,method,properties,body):
    message = json.loads(body)
    print("message", message)
    book_id = message.get("book_id")# Get the book id from the message
    if book_id is not None:
        bok = get_object_or_404(book,id = book_id)# Retrieve the Book object
        if bok.quantity>0:
            bok.quantity -= 1
            bok.save()
    else:
        print("Missing book_id in message:",message)




# Declare and bind queues
declare_queue("book_exchange","borrow_book_queue")

channel.basic_consume(
    queue="borrow_book_queue", on_message_callback=borrow_consumer, auto_ack=True
)

print("Started consuming")
channel.start_consuming()