from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)


class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
