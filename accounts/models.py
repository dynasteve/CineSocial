from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
  bio = models.TextField(blank=True)
  avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
  is_admin = models.BooleanField(default=False)

  def __str__(self):
      return self.username