import requests
from django.conf import settings
from django.core.cache import cache
from movies.models import MovieReview
from django.db.models import Avg, Count

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
        .aggregate(avg=Avg("rating"))
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
        movie["average_rating"] = stats["average_rating"] if stats else None
        movie["review_count"] = stats["review_count"] if stats else 0

    return movies


def get_movie_details(tmdb_id):
    """
    Fetch movie details from TMDB, cache results, and attach local review stats.
    """
    cache_key = f"tmdb_detail_{tmdb_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {"api_key": settings.TMDB_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        movie = response.json()
    except requests.RequestException:
        # Return minimal fallback data if TMDB fails
        return {
            "id": tmdb_id,
            "title": None,
            "overview": None,
            "average_rating": None,
            "review_count": 0
        }

    # Attach review stats
    enriched = _attach_review_stats([movie])
    movie_with_stats = enriched[0]

    # Cache for 1 hour
    cache.set(cache_key, movie_with_stats, timeout=60 * 60)

    return movie_with_stats