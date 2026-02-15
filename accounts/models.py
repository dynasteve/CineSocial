from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
  class Gender(models.TextChoices):
    NONE = 'N', 'Prefer not to say'
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
  
  bio = models.TextField(blank=True, max_length=2000)
  avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
  date_of_birth = models.DateField(blank=False, null=False)
  is_admin = models.BooleanField(default=False)
  gender = models.CharField(choices=Gender.choices, default=Gender.NONE)

  def __str__(self):
      return self.username
    
    
class Follow(models.Model):
  
  user_from = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
  user_to = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  # Checks if a User attempts to follow themselves
  def clean(self):
    if self.user_from == self.user_to:
      raise ValidationError("Users cannot follow themselves.")
    
  def save(self, *args, **kwargs):
    """
    Ensure validation runs before saving to the database.
    full_clean() calls the clean() method above.
    """
    self.full_clean()
    super().save(*args, **kwargs)
    
  class Meta:
    # Prevent duplicate follow relationships
    unique_together = ("user_from", "user_to")

  def __str__(self):
    return f"{self.user_from} -> {self.user_to}"