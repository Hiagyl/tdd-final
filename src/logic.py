# src/logic.py

class BookCatalog:
    def __init__(self):
        # Persistent in-memory data store array
        self.books = []

    def _is_empty(self, value):
        """Helper to sanitize and check for completely empty field string properties."""
        return not value or not str(value).strip()

    def add_book(self, title, author):
        # Cleaned validation sequence utilizing our extracted helper
        if self._is_empty(title) or self._is_empty(author):
            raise ValueError("Title and Author cannot be empty")

        book = {"title": title.strip(), "author": author.strip()}
        self.books.append(book)
        return book

    def remove_book_by_index(self, index):
        # Defensive bounds check boundary mapping
        if index < 0 or index >= len(self.books):
            raise IndexError("Invalid book index mapping")

        return self.books.pop(index)
