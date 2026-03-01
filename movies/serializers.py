from rest_framework import serializers
from .models import *

class MovieReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MovieReview
        fields = ["id", "user", "username", "tmdb_id", "rating", "content", "created_at"]
        read_only_fields = ["id", "user", "username", "created_at"]

    def validate_rating(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Rating must be between 1 and 10")
        return value

class UserMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMovieList
        fields = ["id", "user", "tmdb_id", "list_type", "created_at"]
        read_only_fields = ["id", "user", "created_at"]