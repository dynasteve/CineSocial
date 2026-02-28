from django.db import models
from django.conf import settings


class Post(models.Model):
    """
    Core social post model.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    content = models.TextField(max_length=500)

    image = models.ImageField(
        upload_to="posts/",
        null=True,
        blank=True
    )

    # Self-referencing field for reposts
    original_post = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reposts"
    )

    # Optional future movie attachment
    tmdb_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"