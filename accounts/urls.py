from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name='user_create'),
    path('profiles/<str:username>', ProfileDetailView.as_view(), name='user_profile'),
    path("test/", TestAuthView.as_view()),
]