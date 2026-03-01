from rest_framework import serializers
from .models import MovieReview

class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview
        fields = ["id", "user", "tmdb_id", "rating", "content", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def validate_rating(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Rating must be between 1 and 10")
        return value