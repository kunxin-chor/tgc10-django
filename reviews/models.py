from django.db import models
from books.models import Book
import datetime
from django.contrib.auth.models import User

# Create your models here.


class Review(models.Model):
    title = models.CharField(blank=False, max_length=255)
    content = models.TextField(blank=False)
    date = models.DateField(default=datetime.date.today)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
