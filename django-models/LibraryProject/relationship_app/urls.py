from django.urls import path
from .views import list_books, LibraryDetailView, RegisterView, register, login_view, logout_view, add_book, edit_book, delete_book
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', register, name='register'),
    
    #path('admin-dashboard/',name='admin_dashboard'),
    #path('librarian-dashboard/',name='librarian_dashboard'),
    #path('member-dashboard/',name='member_dashboard'),
    
    path("add-book/", add_book, name="add_book"),
    path("edit-book/<int:book_id>/", edit_book, name="edit_book"),
    path("delete-book/<int:book_id>/", delete_book, name="delete_book"),
]
