from django.db import models

from django.contrib.auth.models import User


class Day(models.Model):
    feel_point = models.PositiveIntegerField(default=5)
    diary_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
