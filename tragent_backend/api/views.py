from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import (GenericAPIView, CreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from . import serializers, models, maps


# For testing
class PingView(GenericAPIView):
    def get(self, request) -> Response:
        return Response('pong', status=status.HTTP_200_OK)


class TripViewSet(ModelViewSet):
    model = models.Trip
    serializer_class = serializers.TripSerializer

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_location(self, request, pk) -> Response:
        # it's necessary, because request.data is is immutable QueryDict
        data = {k: v for k, v in request.data.items()}
        data['trip'] = pk
        serializer = serializers.TripLocationSerializer(
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def delete_location(self, request, pk) -> Response:
        if location_id := request.data.get('location_id'):
            location = get_object_or_404(models.TripLocation, pk=location_id)
            serialized = serializers.TripLocationSerializer(location)
            location.delete()
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def route(self, request, pk) -> HttpResponse:
        trip = self.get_object()
        locations = trip.locations.all()
        if len(locations) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        home = trip.owner.location

        locations = [home, *list(locations)]

        try:
            map_img, distance = maps.generate_route(locations, home)
        except APIException as exc:
            return Response(
                {'detail': exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = HttpResponse(content_type='image/jpg')
        # Yes, I send distance in headers...
        # I know it's a horrible hack, but I don't want to save routes
        # to a database or something, so that's all I came up with
        response.headers['DISTANCE'] = distance
        map_img.save(response, 'JPEG')
        return response


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
    queryset = model.objects.all()

    def get_object(self):
        if not isinstance(self.request.user, AnonymousUser):
            return self.request.user
        else:
            raise NotFound()


class AddLocationView(CreateAPIView):
    model = models.Location
    serializer_class = serializers
