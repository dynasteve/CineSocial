from django.urls import path
from .views import *

urlpatterns = [
  path("search/", MovieSearchView.as_view(), name="movie-search"),
  path("<int:tmdb_id>/", MovieDetailView.as_view(), name="movie-detail"),
  path("<int:tmdb_id>/review/", MovieReviewCreateView.as_view(), name="movie-review-create"),
  path("<int:tmdb_id>/list/", UserMovieListToggleView.as_view(), name="movie-list-toggle"),
  path( "list/<str:list_type>/", UserMovieListView.as_view(), name="movie-list-view"),
]
