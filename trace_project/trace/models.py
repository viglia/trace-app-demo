from django.db import models


class Trace(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    id = models.PositiveIntegerField(primary_key=True)
    trace = models.TextField()
