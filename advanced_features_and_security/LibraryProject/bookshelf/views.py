from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from .models import Book
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Edit logic here

# Use Django ORM to prevent SQL injection
def search_books(request):
    query = request.GET.get('q', '')  # Get the search term from request
    books = Book.objects.filter(title__icontains=query)  # Case-insensitive search
    return render(request, 'bookshelf/book_list.html', {'books': books})
# Create your views here.
