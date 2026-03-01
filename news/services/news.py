import requests
from django.conf import settings

BASE_URL = "https://newsapi.org/v2"


def get_movie_news(query="movies"):
    url = f"{BASE_URL}/everything"

    params = {
        "q": query,
        "apiKey": settings.NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return data.get("articles", [])