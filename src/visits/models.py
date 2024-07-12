from django.db import models

# Create your models here.

class Visits(models.Model):
    path = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField()
