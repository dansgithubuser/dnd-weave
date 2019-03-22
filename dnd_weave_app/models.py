from django.db import models
from django.contrib.auth.models import User

class Secret(models.Model):
    keeper = models.ForeignKey(User, models.CASCADE)
    serialized = models.TextField()
