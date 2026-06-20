from django.db import models
from django.urls import reverse
class Player(models.Model):
    nick = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    best_size = models.IntegerField(default=0)
    hours_played = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    size = models.IntegerField(default=0)
    def __str__(self): return self.nick