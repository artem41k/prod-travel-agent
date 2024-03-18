from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from . import models


# For testing
class PingView(GenericAPIView):
    def get(self, request) -> Response:
        return Response('pong', status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    model = models.User
    serializer_class = serializers.UserSerializer
    queryset = model.objects.all()


class TripViewSet(ModelViewSet):
    model = models.Trip
    serializer_class = serializers.TripSerializer
    queryset = model.objects.all()


class NoteViewSet(ModelViewSet):
    model = models.Note
    serializer_class = serializers.NoteSerializer
    queryset = model.objects.all()
