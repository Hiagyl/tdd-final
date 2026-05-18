class BookCatalog:
    def __init__(self):
        # Persistent in-memory data store array
        self.books = []

    def add_book(self, title, author):
        if not title or not title.strip() or not author or not author.strip():
            raise ValueError("Title and Author cannot be empty")

        book = {"title": title.strip(), "author": author.strip()}
        self.books.append(book)
        return book

    def remove_book_by_index(self, index):
        if index < 0 or index >= len(self.books):
            raise IndexError("Invalid book index mapping")

        return self.books.pop(index)
