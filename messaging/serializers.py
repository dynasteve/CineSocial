from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "created_at", "is_read"]
        read_only_fields = ["id", "sender", "created_at", "is_read"]