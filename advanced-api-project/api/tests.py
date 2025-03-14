from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Author, Book

class BookAPITest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create a test author
        self.author = Author.objects.create(name='Test Author')

        # Authenticate the user
        self.client.login(username='testuser', password='password123')  # ✅ Ensure user is logged in

        # Book creation endpoint
        self.create_url = '/api/books/create/'

    def test_create_book(self):
        """Test creating a book requires authentication"""
        data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': self.author.id  # ✅ Ensure correct author ID is passed
        }
        response = self.client.post(self.create_url, data, format='json')
        print(response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
