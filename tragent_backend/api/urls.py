from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('trips', views.TripViewSet, basename='trip')
router.register('notes', views.NoteViewSet)

urlpatterns = [
    path('ping/', views.PingView.as_view()),
    path('profile/create/', views.CreateUserView.as_view()),
    path('profile/', views.ProfileView.as_view()),
]

urlpatterns += router.urls
