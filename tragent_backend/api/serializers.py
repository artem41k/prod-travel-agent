from rest_framework import serializers, exceptions

from .maps import OSM
from .models import User, Trip, Note, UserLocation, TripLocation


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ['name', 'lat', 'lon']


class TripLocationSerializer(serializers.ModelSerializer):
    query = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = TripLocation
        fields = [
            'name', 'query', 'lat', 'lon',
            'trip', 'start_date', 'end_date'
        ]
        extra_kwargs = {
            'name': {'read_only': True},
            'lat': {'required': False},
            'lon': {'required': False},
        }

    def validate_query(self, value: str) -> UserLocation:
        """ Validate query if it was provided in request body as text """
        city, country, data = OSM().get_city_by_name(value)
        if data:
            return TripLocation(
                city=city,
                country=country,
                lat=data['lat'],
                lon=data['lon'],
                data=data
            )
        else:
            raise exceptions.NotFound('Location not found')

    def validate(self, attrs: dict) -> dict:
        """ Validate location if it was provided as lat & lon
            (and validate if there are any location params or not)
        """
        if (lat := attrs.get('lat')) and (lon := attrs.get('lon')):
            city, country, data = OSM().get_city_by_coords(lat, lon)
            attrs['location'] = TripLocation(
                city=city,
                country=country,
                lat=data['lat'],
                lon=data['lon'],
                data=data
            )
        elif location := attrs.get('query'):
            attrs['location'] = location
        else:
            raise serializers.ValidationError(
                'You must provide either location or lat and lon'
            )
        return attrs

    def create(self, validated_data: dict) -> TripLocation:
        trip_location = validated_data['location']
        trip_location.start_date = validated_data['start_date']
        trip_location.end_date = validated_data['end_date']
        trip_location.trip = validated_data['trip']
        trip_location.save()
        return trip_location


class UserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(required=False)
    name = serializers.CharField(read_only=True)
    location = serializers.CharField(
        source='location.name', required=False
    )
    lat = serializers.FloatField(required=False, write_only=True)
    lon = serializers.FloatField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'tg_id', 'first_name', 'last_name',
            'name', 'age', 'location', 'lat', 'lon', 'bio'
        ]

    def validate(self, attrs: dict) -> dict:
        """ Validate location if it was provided as lat & lon
            (and validate if there are any location params or not)
        """
        if (lat := attrs.get('lat')) and (lon := attrs.get('lon')):
            city, country, data = OSM().get_city_by_coords(lat, lon)
            attrs['location'] = UserLocation(
                city=city,
                country=country,
                lat=data['lat'],
                lon=data['lon'],
                data=data
            )
        elif not attrs.get('location'):
            raise serializers.ValidationError(
                'You must provide either location or lat and lon'
            )
        return attrs

    def validate_location(self, value: str) -> UserLocation:
        """ Validate location if it was provided in request body as text """
        city, country, data = OSM().get_city_by_name(value)
        if data:
            return UserLocation(
                city=city,
                country=country,
                lat=data['lat'],
                lon=data['lon'],
                data=data
            )
        else:
            raise serializers.ValidationError('Invalid location')

    def create(self, validated_data) -> User:
        location = validated_data.pop('location')
        validated_data.pop('lat')  # remove unnecessary keys
        validated_data.pop('lon')

        user = User.objects.create(**validated_data)
        # Only to register users from telegram
        # (see "Future expansion" section in README)
        user.set_unusable_password()

        location.user = user
        location.save()
        return user


class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = '__all__'

    def validate(self, attrs: dict) -> dict:
        attrs['owner'] = self.context['request'].user
        return attrs


class TripSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    participants = UserSerializer(read_only=True, many=True)
    locations = TripLocationSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'name', 'description', 'owner', 'start_date', 'end_date',
            'participants', 'locations', 'notes'
        ]

    def validate(self, attrs: dict) -> dict:
        attrs['owner'] = self.context['request'].user
        return attrs
