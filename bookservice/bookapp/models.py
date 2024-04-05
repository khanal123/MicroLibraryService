from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .bookproducer import BookProducer
# Create your models here.

class book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 100)
    summary = models.TextField()
    publication_date = models.DateField()
    isbn = models.CharField(max_length = 13)
    pages = models.IntegerField()
    cover = models.TextField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title   

@receiver(post_save,sender = book)
def book_action(sender,instance,created,**kwargs):
    if created:
        book_data = {
            "title" : instance.title,
            "author" : instance.author,
            "summary" : instance.summary,
            "publication_date" : instance.publication_date.strftime("%Y-%m-%d"),
            "isbn" : instance.isbn,
            "pages" : instance.pages,
            "cover" : instance.cover,
            "quantity" : instance.quantity,
        }

        # Calling the book producer with the extracted book data
        BookProducer(book_data)

