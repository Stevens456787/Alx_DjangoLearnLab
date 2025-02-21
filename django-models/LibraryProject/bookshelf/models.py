from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
    
# filepath: /c:/Users/Rnyamari/Desktop/DJ LEARN/Alx_DjangoLearnLab/django-models/LibraryProject/bookshelf/models.py
from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name