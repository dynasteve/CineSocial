from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "created_at", "is_read"]
        read_only_fields = ["id", "sender", "created_at", "is_read"]
        
        def perform_create(self, serializer):
            receiver = serializer.validated_data["receiver"]

            if receiver == self.request.user:
                raise ValidationError("Cannot message yourself.")

            serializer.save(sender=self.request.user)