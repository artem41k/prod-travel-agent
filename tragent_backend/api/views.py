from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotFound
from rest_framework.generics import (GenericAPIView, CreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from . import serializers
from . import models


# For testing
class PingView(GenericAPIView):
    def get(self, request) -> Response:
        return Response('pong', status=status.HTTP_200_OK)


class TripViewSet(ModelViewSet):
    model = models.Trip
    serializer_class = serializers.TripSerializer

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class NoteViewSet(ModelViewSet):
    model = models.Note
    serializer_class = serializers.NoteSerializer
    queryset = model.objects.all()


class CreateUserView(CreateAPIView):
    model = models.User
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]


class ProfileView(RetrieveUpdateAPIView):
    model = models.User
    serializer_class = serializers.UserSerializer

    def get_object(self):
        if not isinstance(self.request.user, AnonymousUser):
            return self.request.user
        else:
            raise NotFound()


class AddLocationView(CreateAPIView):
    model = models.Location
    serializer_class = serializers
