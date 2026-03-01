from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class PostCreateView(generics.CreateAPIView):
    """
    Create a new post.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()
      
      
class PostLikeToggleView(APIView):
    """
    Toggle like/unlike for a post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()
            return Response({"liked": False})

        return Response({"liked": True})
      

class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

class CommentCreateView(generics.CreateAPIView):
  """
  Create a new comment on a post.
  """
  serializer_class = CommentSerializer
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    post_id = self.kwargs.get("post_id")
    post = get_object_or_404(Post, id=post_id)
    serializer.save(
      author=self.request.user,
      post=post  # pass instance, not _id
    )
    
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "like_count", "comment_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        following_ids = user.following.values_list("user_to", flat=True)

        return (
            Post.objects
            .filter(author__id__in=following_ids)
            .annotate(
                like_count=Count("likes"),
                comment_count=Count("comments"),
            )
        )
      
      
def get_queryset(self):
    user = self.request.user
    following_ids = user.following.values_list("user_to", flat=True)

    return (
        Post.objects
        .filter(author__id__in=following_ids)
        .annotate(
            like_count=Count("likes"),
            comment_count=Count("comments")
        )
    )
    
    
class PostRepostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        original_post = get_object_or_404(Post, pk=pk)

        repost = Post.objects.create(
            author=request.user,
            original_post=original_post,
            content=request.data.get("content", "")
        )

        serializer = PostSerializer(repost, context={"request": request})
        return Response(serializer.data)