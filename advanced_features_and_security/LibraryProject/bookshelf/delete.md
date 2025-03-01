
#### **`delete.md`**
```md
# Delete a Book Entry

## Command:
```python
from bookshelf.models import Book
book.delete()
print(Book.objects.all())  # Should return an empty queryset
