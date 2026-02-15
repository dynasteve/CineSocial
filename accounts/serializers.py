from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  """
  Serializer to obtain user information
  """
  follower_count = serializers.SerializerMethodField()
  following_count = serializers.SerializerMethodField()
  
  class Meta:
    model = User
    fields = [
            "id",
            "username",
            "email",
            "bio",
            "avatar",
            "date_of_birth",
            "gender",
            "follower_count",
            "following_count",
        ]
    read_only_fields = ["id", "follower_count", "following_count"]
    
  def get_follower_count(self, obj):
    return obj.followers.count()
  
  def get_following_count(self, obj):
    return obj.following.count()
  

class RegisterSerializer(serializers.ModelSerializer):
  """
  Serializer for User creation/registration
  """
  
  password = serializers.CharField(write_only=True, required=True, min_length=8)
  password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")
  
  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'password2', 'bio', 'avatar', 'date_of_birth', 'gender']
    
  def validate(self, data):
    if data['password'] != data['password2']:
      raise serializers.ValidationError("Passwords must match")
    
    # Use django in-built password validators
    validate_password(data['password'])
    return data
  
  def create(self, validated_data):
    validated_data.pop('password2')
    password = validated_data.pop('password')
    user = User(**validated_data)
    user.set_password(password)
    user.save()
    return user