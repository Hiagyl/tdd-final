import pytest
from src.logic import BookCatalog


def test_unit_add_book_validation_error():
    catalog = BookCatalog()

    # Validation Rule: Preventing empty string titles or authors
    with pytest.raises(ValueError, match="Title and Author cannot be empty"):
        catalog.add_book("", "George Orwell")


def test_unit_remove_book_successfully():
    """Test 1: Valid index removal shifts and reduces the catalog count properly."""
    catalog = BookCatalog()
    catalog.add_book("1984", "George Orwell")
    catalog.add_book("Brave New World", "Aldous Huxley")

    # Act: Attempt to remove the first book
    removed_book = catalog.remove_book_by_index(0)

    # Assert: Check that the correct book data was popped and the array length updated
    assert removed_book["title"] == "1984"
    assert len(catalog.books) == 1
    assert catalog.books[0]["title"] == "Brave New World"


def test_unit_remove_book_index_out_of_bounds_high():
    """Test 2: Requesting an index higher than the catalog list length raises an IndexError."""
    catalog = BookCatalog()
    catalog.add_book("Dune", "Frank Herbert")

    # Assert: Index 5 does not exist, so it must raise a clean IndexError mapping error
    with pytest.raises(IndexError, match="Invalid book index mapping"):
        catalog.remove_book_by_index(5)


def test_unit_remove_book_index_negative():
    """Test 3: Requesting a negative index boundary ranges raises an IndexError."""
    catalog = BookCatalog()
    catalog.add_book("Dune", "Frank Herbert")

    # Assert: Negative indexing should be blocked to prevent unexpected deletions
    with pytest.raises(IndexError, match="Invalid book index mapping"):
        catalog.remove_book_by_index(-1)
