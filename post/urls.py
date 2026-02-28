from django.urls import path
from .views import PostCreateView, PostLikeToggleView, CommentCreateView

urlpatterns = [
    path("posts/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/like/", PostLikeToggleView.as_view(), name="post-like-toggle"),
    path("posts/<int:post_id>/comment/", CommentCreateView.as_view(), name="post-comment"),
]