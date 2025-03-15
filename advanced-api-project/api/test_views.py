from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Author, Book

class BookAPITest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create a test author
        self.author = Author.objects.create(name='Test Author')
        
        # Create a test book
        self.book = Book.objects.create(title='Test Book', publication_year=2023, author=self.author)
        
        # API Endpoints
        self.book_list_url = '/api/books/'
        self.book_detail_url = f'/api/books/{self.book.id}/'
    
    def test_create_book(self):
        data = {'title': 'New Book', 'publication_year': 2024, 'author': self.author.id}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_retrieve_book(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_update_book(self):
        data = {'title': 'Updated Book', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
    
    def test_delete_book(self):
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_filter_books_by_title(self):
        response = self.client.get(self.book_list_url, {'title': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_books(self):
        response = self.client.get(self.book_list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_order_books_by_year(self):
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
