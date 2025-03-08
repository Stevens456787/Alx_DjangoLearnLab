#from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.generics import ModelViewSet
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
