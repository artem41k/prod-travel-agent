from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime


class User(AbstractUser):
    username = None
    tg_id = models.BigIntegerField(null=True, unique=True)
    age = models.PositiveIntegerField(null=True)
    bio = models.TextField(null=True)

    USERNAME_FIELD = 'tg_id'

    @property
    def name(self) -> str:
        return self.get_full_name()


class Trip(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='trips'
    )
    participants = models.ManyToManyField(
        User, related_name='participating_trips'
    )

    @property
    def start_date(self) -> datetime.date | None:
        if len(locations := self.locations.all()) > 0:
            return min(locations.values_list('start_date'))[0]

    @property
    def end_date(self) -> datetime.date | None:
        if len(locations := self.locations.all()) > 0:
            return max(locations.values_list('end_date'))[0]


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


class Location(models.Model):
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    lat = models.FloatField()
    lon = models.FloatField()
    data = models.JSONField()  # Stores OpenStreetMap Nominatim data

    class Meta:
        abstract = True

    @property
    def name(self) -> str:
        return ', '.join([self.city, self.country])


class UserLocation(Location):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='location'
    )


class TripLocation(Location):
    start_date = models.DateField()
    end_date = models.DateField()
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE,
        related_name='locations', null=True
    )

    class Meta:
        ordering = ['start_date']
