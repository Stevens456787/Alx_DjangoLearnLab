from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    additional_info = models.TextField(blank=True, null=True) 
    
    
    def __str__(self):
        return self.username