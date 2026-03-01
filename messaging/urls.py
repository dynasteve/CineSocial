from django.urls import path
from .views import *

urlpatterns = [
  path("send/", SendMessageView.as_view(), name="send-message"),
  path("inbox/", InboxView.as_view(), name="inbox"),
  path("conversation/<int:user_id>/", ConversationView.as_view(), name="conversation"),
]
