from django.urls import path
from .views import *

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/like/", PostLikeToggleView.as_view(), name="post-like-toggle"),
    path("posts/<int:post_id>/comment/", CommentCreateView.as_view(), name="post-comment"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
    path("posts/<int:pk>/repost/", PostRepostView.as_view(), name="post-repost"),
]