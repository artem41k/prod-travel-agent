from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    tg_id = models.BigIntegerField(null=True, unique=True)
    age = models.PositiveIntegerField(null=True)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    bio = models.TextField(null=True)

    USERNAME_FIELD = 'tg_id'

    @property
    def name(self) -> str:
        return self.get_full_name()


class Trip(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='trips'
    )
    participants = models.ManyToManyField(
        User, related_name='participating_trips'
    )


class Note(models.Model):
    text = models.TextField()
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='notes'
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE, related_name='notes'
    )
