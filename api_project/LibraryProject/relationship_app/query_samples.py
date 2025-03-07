import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query: Get all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return books

# Query: List all books in a library
def list_books_in_library(library_name):
    library = Library.objects.get(name=library_name)  # <-- MISSING QUERY ADDED HERE
    return library.books.all()

# Query: Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)

# Test the queries (if running this file directly)
if __name__ == "__main__":
    author_name = "J.K. Rowling"
    library_name = "Central Library"

    try:
        books = get_books_by_author(author_name)
        print(f"Books by {author_name}: {[book.title for book in books]}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")

    try:
        books_in_library = list_books_in_library(library_name)
        print(f"Books in {library_name}: {[book.title for book in books_in_library]}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

    try:
        librarian = get_librarian_for_library(library_name)
        print(f"Librarian for {library_name}: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print(f"Librarian or Library '{library_name}' not found.")
