from django.urls import path
from .views import PostCreateView, PostLikeToggleView

urlpatterns = [
    path("posts/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/like/", PostLikeToggleView.as_view(), name="post-like-toggle"),
]