from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services.tmdb import search_movies, get_movie_details


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