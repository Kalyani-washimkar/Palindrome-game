from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=100, unique=True)
    board = models.CharField(max_length=100, default="", blank=True)
    is_completed = models.BooleanField(default=False)
    is_palindrome = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True, auto_created=True)