from django.urls import path
from .views import list_books, LibraryDetailView, register, login_view, logout_view
from django.contrib.auth.views import LoginView, LogoutView
from .import views
from django.contrib.auth import views as auth_views
from .views import RegisterView
from .views import admin_view, librarian_view, member_view
from .views import add_book, edit_book, delete_book



urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/',RegisterView.as_view(), name='register'),
    
    path('admin-dashboard/', admin_view.admin_dashboard, name='admin_dashboard'),
    path('librarian-dashboard/', librarian_view.librarian_dashboard, name='librarian_dashboard'),
    path('member-dashboard/', member_view.member_dashboard, name='member_dashboard'),
    
     path("add-book/", add_book, name="add_book"),
    path("edit-book/<int:book_id>/", edit_book, name="edit_book"),
    path("delete-book/<int:book_id>/", delete_book, name="delete_book"),
]
