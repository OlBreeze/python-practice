from django.db import models


class Server(models.Model):
    STATUS_CHOICES = [
        ('online', 'Увімкнений'),
        ('offline', 'Вимкнений'),
    ]
    name = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='online')
    created_at = models.DateTimeField(auto_now_add=True)


class ServerMetric(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Alert(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    message = models.TextField()
    is_critical = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
