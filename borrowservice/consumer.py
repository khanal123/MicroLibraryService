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

sys.path.append(str(BASE_DIR / "borrowservice"))

path.append(BASE_DIR / "borrowservice/settings.py")
os.environ.setdefault("DJANGO_SETTINGS_MODULE","borrowservice.settings")
django.setup()

from borrow.models import Borrow,Books

# RabbitMQ details
RABBITMQ_URL = settings.RABBITMQ_URL
params = pika.URLParameters(RABBITMQ_URL)

# Establish connection to cloudamqp
connection = pika.BlockingConnection(params)
channel = connection.channel()

def declare_queue(exchange_name, queue_name):
    channel.exchange_declare(exchange= exchange_name, exchange_type= "fanout")
    result = channel.queue_declare(queue= queue_name)
    queue_name = result.method.queue
    channel.queue_bind(exchange= exchange_name, queue= queue_name)

def borrow_consumer(channel,method,properties,body):
    message = json.loads(body)
    print(message)
    save = Borrow.objects.create(
        user_id = message.get("user_id"),
        book_id = message.get("book_id"),
        borrow_date = message.get("borrow_date"),
        # due_date = message.get("due_date"),
        # returned = message.get("returned"),
        return_date = message.get("return_date")
    )
    print(save)

    if save:
        print("Borrow saved successfully")

def book_consumer(channel,method,properties,body):
    message = json.loads(body)
    save = Books.objects.create(
        title = message["title"],
        author = message["author"],
        summary = message["summary"],
        publication_date = message["publication_date"],
        isbn = message["isbn"],
        pages = message["pages"],
        cover = message["cover"],
        quantity = message["quantity"],
    )
    if save:
        print("Book saved successfully")

# Declare and bind queues
declare_queue("borrow_exchange","borrow_queue")
declare_queue("book_exchange","book_queue")

channel.basic_consume(
    queue= "borrow_queue", on_message_callback= borrow_consumer ,auto_ack= True
)

channel.basic_consume(
    queue= "book_queue", on_message_callback= book_consumer , auto_ack= True
)

print("Consuming ...")
channel.start_consuming()