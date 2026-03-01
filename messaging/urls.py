from django.urls import path
from .views import *

urlpatterns = [
  path("send/", SendMessageView.as_view(), name="send-message"),
  path("inbox/", InboxView.as_view(), name="inbox"),
  path("conversation/<int:user_id>/", ConversationView.as_view(), name="conversation"),
  path("<int:pk>/read/", MarkAsReadView.as_view(), name="mark-as-read"),
  path("unread-count/", UnreadCountView.as_view(), name="unread-count"),
]
