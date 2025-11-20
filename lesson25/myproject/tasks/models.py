from django.db import models
from django.contrib.auth.models import User


# 1. Task Manager
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Не виконано'),
        ('done', 'Виконано'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title