from django.db import models
from django.conf import settings

class MovieReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="movie_reviews"
    )
    tmdb_id = models.IntegerField()  # only store TMDB ID
    rating = models.PositiveSmallIntegerField(db_index=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tmdb_id")  # one review per user per movie
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - TMDB {self.tmdb_id} - {self.rating}"
      

class UserMovieList(models.Model):
    LIST_TYPES = (
        ("favorite", "Favorite"),
        ("watchlist", "Watchlist"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="movie_lists"
    )
    tmdb_id = models.IntegerField(db_index=True)
    list_type = models.CharField(max_length=20, choices=LIST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tmdb_id", "list_type")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.list_type} - {self.tmdb_id}"