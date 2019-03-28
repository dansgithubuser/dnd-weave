from . import models

from rest_framework import serializers

class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Secret
        fields = ('id', 'name', 'serialized')
