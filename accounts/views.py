from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

class RegisterView(CreateAPIView):
  """
  User registration endpoint
  """
  serializer_class = RegisterSerializer
  permission_classes = [AllowAny]

class TestAuthView(APIView):
  def get(self, req):
    return Response({"message": "Authenticated successfully"})