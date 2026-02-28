from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser, Follow


User = get_user_model()

class RegisterView(CreateAPIView):
  """
  User registration endpoint
  """
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  permission_classes = [AllowAny]
  

class ProfileDetailView(RetrieveAPIView):
  """
  Users Profile GET endpoint by username
  """
  serializer_class = UserSerializer
  lookup_field = 'username'
  queryset = User.objects.all()
  permission_classes = [AllowAny]
  

class FollowToggleView(APIView):
  """
  Makes a user follow/unfollow another user
  """
  
  permission_classes = [IsAuthenticated]
  
  def post(self, request, username):
    current_user = request.user
    target_user = get_object_or_404(User, username=username)
    
    # API level check for users following themselves
    if target_user == current_user:
      return Response(
        {'message': "User cannot follow themselves"}, status=400
      )
    
    try:
      # Try to fetch existing follows
      follow = Follow.objects.get(user_from=current_user, user_to=target_user)
      # If it exists → unfollow
      follow.delete()
      return Response({"following": False})
    except:
           # If it doesn’t exist → follow
            Follow.objects.create(user_from=current_user, user_to=target_user)
            return Response({"following": True})


class TestAuthView(APIView):
  def get(self, req):
    return Response({"message": "Authenticated successfully"})
  