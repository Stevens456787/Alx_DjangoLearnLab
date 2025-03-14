from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Author, Book

class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book_data = {"title": "Harry Potter", "publication_year": 2000, "author": self.author.id}

    def test_create_book(self):
        response = self.client.post(reverse('book-list'), self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_books(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
