from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name='user_create'),
    path('profiles/<str:username>', ProfileDetailView.as_view(), name='user_profile'),
    path("profiles/<str:username>/follow/", FollowToggleView.as_view(), name='follow-toggle'),
    path("test/", TestAuthView.as_view()),
]