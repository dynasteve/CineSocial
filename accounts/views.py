from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser


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
  

class TestAuthView(APIView):
  def get(self, req):
    return Response({"message": "Authenticated successfully"})