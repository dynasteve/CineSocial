from django.urls import path
from .views import *

urlpatterns = [
  path("", MovieNewsView.as_view(), name="movie-news"),
]
