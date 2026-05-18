# src/logic.py

class BookCatalog:
    def __init__(self):
        self.books = []

    def _is_empty(self, value):
        """Helper to sanitize and check for completely empty field string properties."""
        return not value or not str(value).strip()

    def add_book(self, title, author):
        if self._is_empty(title) or self._is_empty(author):
            raise ValueError("Title and Author cannot be empty")

        book = {"title": title.strip(), "author": author.strip()}
        self.books.append(book)
        return book

    def update_book_by_index(self, index, title, author):
        """Helper to cleanly validate and update a book structure by its index."""
        if self._is_empty(title) or self._is_empty(author):
            raise ValueError("Title and Author cannot be empty")

        if index < 0 or index >= len(self.books):
            raise IndexError("Invalid book index mapping")

        self.books[index] = {"title": title.strip(), "author": author.strip()}
        return self.books[index]

    def remove_book_by_index(self, index):
        if index < 0 or index >= len(self.books):
            raise IndexError("Invalid book index mapping")

        return self.books.pop(index)
