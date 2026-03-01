from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        
        
class InboxView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            receiver=self.request.user
        )
        
class ConversationView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.kwargs["user_id"]

        return Message.objects.filter(
            Q(sender=self.request.user, receiver_id=other_user_id) |
            Q(sender_id=other_user_id, receiver=self.request.user)
        )
        
class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            message = Message.objects.get(pk=pk, receiver=request.user)
        except Message.DoesNotExist:
            return Response(
                {"detail": "Message not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        message.is_read = True
        message.save()

        return Response(
            {"detail": "Message marked as read."},
            status=status.HTTP_200_OK
        )
        

class UnreadCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()

        return Response({"unread_count": count})