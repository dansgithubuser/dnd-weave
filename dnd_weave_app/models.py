from django.db import models
from django.contrib.auth.models import User

import weave

class SecretManager(models.Manager):
    def create(self, **kwargs):
        kwargs['serialized'] = weave.Secret().serialize()
        return models.Manager.create(self, **kwargs)

class Secret(models.Model):
    name = models.TextField(null=True)
    keeper = models.ForeignKey(User, models.CASCADE)
    serialized = models.TextField()

    objects = SecretManager()

class Character(models.Model):
    name = models.TextField()
    player = models.ForeignKey(User, models.CASCADE)
    secret = models.ForeignKey(Secret, models.PROTECT, null=True)

class Spell(models.Model):
    character = models.ForeignKey(Character, models.CASCADE)
    ciphertext = models.BinaryField()
    learned = models.BooleanField()
    level = models.IntegerField()

class Offer(models.Model):
    secret = models.ForeignKey(Secret, models.CASCADE)
    character = models.ForeignKey(Character, models.CASCADE)
