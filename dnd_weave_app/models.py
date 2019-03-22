from django.db import models
from django.contrib.auth.models import User

import weave

class SecretManager(models.Manager):
    def create(self, **kwargs):
        kwargs['serialized'] = weave.Secret().serialize()
        return models.Manager.create(self, **kwargs)

class Secret(models.Model):
    keeper = models.ForeignKey(User, models.CASCADE)
    serialized = models.TextField()

    objects = SecretManager()
