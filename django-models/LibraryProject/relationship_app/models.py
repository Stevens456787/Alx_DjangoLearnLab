from django.contrib.auth.models import User
from django.db import models
# filepath: /c:/Users/Rnyamari/Desktop/DJ LEARN/Alx_DjangoLearnLab/django-models/LibraryProject/relationship_app/views.py
from bookshelf.models import Book, Library

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField()

    def __str__(self):
        return self.title

