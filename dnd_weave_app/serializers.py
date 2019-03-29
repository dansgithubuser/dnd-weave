from . import models

from rest_framework import serializers

class SecretSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    serialized = serializers.CharField(required=False)

    class Meta:
        model = models.Secret
        fields = ('id', 'name', 'serialized')

class CharacterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = models.Character
        fields = ('id', 'name', 'secret_id')
