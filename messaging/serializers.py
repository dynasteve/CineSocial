from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    sender_id = serializers.IntegerField(source='sender.id', read_only=True)  # ADD - frontend needs this

    class Meta:
        model = Message
        fields = ["id", "sender", "sender_id", "receiver", "content", "created_at", "is_read"]
        read_only_fields = ["id", "sender", "sender_id", "created_at", "is_read"]

    def validate_receiver(self, value):                    # MOVED OUT of Meta
        request = self.context.get("request")
        if request and value == request.user:
            raise ValidationError("Cannot message yourself.")
        return value