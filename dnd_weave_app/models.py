from django.db import models
from django.contrib.auth.models import User

class Secret(models.Model):
    name = models.TextField(null=True)
    keeper = models.ForeignKey(User, models.CASCADE)
    serialized = models.TextField()

class Character(models.Model):
    name = models.TextField(null=True)
    player = models.ForeignKey(User, models.CASCADE)
    secret = models.ForeignKey(Secret, models.PROTECT, null=True)

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

class Spell(models.Model):
    character = models.ForeignKey(Character, models.CASCADE)
    runes = models.TextField(default='')
    dict = models.TextField(null=True)

class Offer(models.Model):
    secret = models.ForeignKey(Secret, models.CASCADE)
    character = models.ForeignKey(Character, models.CASCADE)
