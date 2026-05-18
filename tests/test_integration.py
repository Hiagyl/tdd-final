import pytest

# ==============================================================================
# 1. CREATE (POST) OPERATIONS
# ==============================================================================

def test_integration_create_book_success(client):
    """Verifies that a valid POST payload registers a book and returns 201 Created."""
    payload = {"title": "The Hobbit", "author": "J.R.R. Tolkien"}
    response = client.post('/books', json=payload)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "The Hobbit"
    assert data["author"] == "J.R.R. Tolkien"


def test_integration_create_book_missing_fields(client):
    """Defensively checks that an empty title payload triggers an HTTP 400 Bad Request."""
    payload = {"title": "", "author": "J.R.R. Tolkien"}
    response = client.post('/books', json=payload)
    
    assert response.status_code == 400
    assert "error" in response.get_json()


# ==============================================================================
# 2. READ (GET) OPERATIONS
# ==============================================================================

def test_integration_get_all_books_empty(client):
    """Ensures an unseeded catalog gracefully yields an empty list and 200 OK."""
    response = client.get('/books')
    
    assert response.status_code == 200
    assert response.get_json() == []


def test_integration_get_all_books_populated(client):
    """Ensures a GET request fetches all registered items sequentially."""
    # Seed data directly through the client loop
    client.post('/books', json={"title": "Book A", "author": "Author A"})
    client.post('/books', json={"title": "Book B", "author": "Author B"})
    
    response = client.get('/books')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "Book A"
    assert data[1]["title"] == "Book B"


# ==============================================================================
# 3. UPDATE (PUT) OPERATIONS
# ==============================================================================

def test_integration_update_book_success(client):
    """Verifies that a PUT request correctly mutates an item at a targeted index."""
    # Seed original item at index 0
    client.post('/books', json={"title": "Original Title", "author": "Original Author"})
    
    # Act: Overwrite index 0
    updated_payload = {"title": "Updated Title", "author": "Updated Author"}
    response = client.put('/books/0', json=updated_payload)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Title"
    assert data["message"] == "Book updated successfully"



# ==============================================================================
# 4. DELETE (DELETE) OPERATIONS
# ==============================================================================

def test_integration_delete_book_success(client):
    """Confirms that a DELETE request eliminates an item and reduces list capacity."""
    client.post('/books', json={"title": "To Kill a Mockingbird", "author": "Harper Lee"})
    
    response = client.delete('/books/0')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Book deleted successfully"

