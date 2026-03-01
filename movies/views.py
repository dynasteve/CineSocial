from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services.tmdb import search_movies, get_movie_details
from .serializers import *
from .models import *


class MovieSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            return Response({"error": "Query parameter required"}, status=400)

        data = search_movies(query)
        return Response(data)


class MovieDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tmdb_id):
        data = get_movie_details(tmdb_id)
        return Response(data)
      

class MovieReviewCreateView(CreateAPIView):
    serializer_class = MovieReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        tmdb_id = serializer.validated_data["tmdb_id"]

        # Try to get existing review
        review, created = MovieReview.objects.update_or_create(
            user=user,
            tmdb_id=tmdb_id,
            defaults={
                "rating": serializer.validated_data["rating"],
                "content": serializer.validated_data.get("content", "")
            }
        )
        return review

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = self.perform_create(serializer)
        return Response(
            MovieReviewSerializer(review, context={"request": request}).data,
            status=status.HTTP_200_OK
        )
        
        
class UserMovieListToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tmdb_id):
        list_type = request.data.get("list_type")

        if list_type not in ["favorite", "watchlist"]:
            return Response({"error": "Invalid list type"}, status=400)

        obj, created = UserMovieList.objects.get_or_create(
            user=request.user,
            tmdb_id=tmdb_id,
            list_type=list_type
        )

        if not created:
            obj.delete()
            return Response({"added": False})

        return Response({"added": True})
      
      
class UserMovieListView(ListAPIView):
    serializer_class = UserMovieListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list_type = self.kwargs["list_type"]
        return UserMovieList.objects.filter(
            user=self.request.user,
            list_type=list_type
        )