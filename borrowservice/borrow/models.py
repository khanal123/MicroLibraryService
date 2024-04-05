from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime

# Create your models here.


class Borrow(models.Model):
    user_id = models.IntegerField(null= True)
    book_id = models.IntegerField()
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)


class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    summary = models.TextField()
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    cover = models.TextField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title
