from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    """

    author = serializers.StringRelatedField(read_only=True)

    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    repost_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "image",
            "tmdb_id",
            "original_post",
            "like_count",
            "comment_count",
            "repost_count",
            "is_liked",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "author",
            "like_count",
            "comment_count",
            "repost_count",
            "is_liked",
            "created_at",
        ]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_repost_count(self, obj):
        return obj.reposts.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")

        if request is None or request.user.is_anonymous:
            return False

        return obj.likes.filter(user=request.user).exists()

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)