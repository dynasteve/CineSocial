import requests
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"


def search_movies(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": query,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_movie_details(tmdb_id):
    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()