from rest_framework import serializers

from .models import User, Trip, Note


class UserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(required=False)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'tg_id', 'first_name', 'last_name',
            'name', 'age', 'city', 'country', 'bio'
        ]

    def create(self, validated_data) -> User:
        user = User.objects.create(**validated_data)
        # Only to register users from telegram
        # (see "Future expansion" section in README)
        user.set_unusable_password()
        return user


class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner = serializers.IntegerField(write_only=True)

    class Meta:
        model = Note
        fields = '__all__'

    def validate_owner(self, value: int) -> User:
        user = User.objects.filter(pk=value).first()
        if user:
            return user
        else:
            raise serializers.ValidationError


class TripSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner = serializers.IntegerField(write_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Trip
        fields = '__all__'

    def validate_owner(self, value: int) -> User:
        user = User.objects.filter(pk=value).first()
        if user:
            return user
        else:
            raise serializers.ValidationError
