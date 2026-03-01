import requests
from django.conf import settings
from django.db.models import Avg, Count
from movies.models import MovieReview

BASE_URL = "https://api.themoviedb.org/3"


def _attach_review_stats(movies):
    """
    Accepts a list of movie dictionaries and injects
    average_rating + review_count from local DB.
    """
    if not movies:
        return movies

    tmdb_ids = [movie["id"] for movie in movies]

    review_stats = (
        MovieReview.objects
        .filter(tmdb_id__in=tmdb_ids)
        .values("tmdb_id")
        .annotate(
            average_rating=Avg("rating"),
            review_count=Count("id")
        )
    )

    stats_map = {
        item["tmdb_id"]: {
            "average_rating": round(item["average_rating"], 2),
            "review_count": item["review_count"]
        }
        for item in review_stats
    }

    for movie in movies:
        stats = stats_map.get(movie["id"])
        movie["average_rating"] = (
            stats["average_rating"] if stats else None
        )
        movie["review_count"] = (
            stats["review_count"] if stats else 0
        )

    return movies


def search_movies(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": query,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    data["results"] = _attach_review_stats(results)

    return data


def get_movie_details(tmdb_id):
    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    movie = response.json()

    # Wrap single movie in list for reuse of helper
    enriched = _attach_review_stats([movie])
    return enriched[0]