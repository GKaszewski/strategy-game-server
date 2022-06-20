import uuid as uuid
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)

    wood = models.PositiveIntegerField(default=0)
    iron = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)

    wood_per_minute = models.PositiveIntegerField(default=0)
    iron_per_minute = models.PositiveIntegerField(default=0)
    gold_per_minute = models.PositiveIntegerField(default=0)

    admin_points = models.PositiveIntegerField(default=0)
    diplomacy_points = models.PositiveIntegerField(default=0)
    military_points = models.PositiveIntegerField(default=0)

    admin_points_per_minute = models.PositiveIntegerField(default=0)
    diplomacy_points_per_minute = models.PositiveIntegerField(default=0)
    military_points_per_minute = models.PositiveIntegerField(default=0)

    manpower = models.PositiveIntegerField(default=100)

    def __str__(self):
        if self.user:
            return self.user.username
        return 'user not found lol'


class PlayerSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Player
        lookup_field = 'uuid'
        fields = '__all__'
        extra_kwargs = {"user": {"required": False, "allow_null": True}}

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.filter(username=user_data).first()
        if not user:
            raise serializers.ValidationError('User doesnt exists!')
        player, created = Player.objects.get_or_create(user=user, **validated_data)
        if created:
            player.user = user
            player.save()
            return player
        else:
            raise serializers.ValidationError('Player already exists!')
