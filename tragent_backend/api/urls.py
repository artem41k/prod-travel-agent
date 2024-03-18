from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('users', views.UserViewSet)
router.register('trips', views.TripViewSet)
router.register('notes', views.NoteViewSet)

urlpatterns = [
    path('ping/', views.PingView.as_view()),
]

urlpatterns += router.urls
