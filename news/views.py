from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .services.news import get_movie_news


class MovieNewsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "movies")
        articles = get_movie_news(query=query)

        return Response({
            "count": len(articles),
            "results": articles
        })