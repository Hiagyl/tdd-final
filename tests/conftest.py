import pytest
from src.app import create_app, books


@pytest.fixture(scope="session")
def app():
    """Initializes the Flask application wrapper instance for testing engines."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app


@pytest.fixture()
def client(app):
    """Provides a functional mock HTTP client to simulate network requests."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clear_global_state():
    """Automatically flushes the in-memory array data before every single test."""
    books.clear()
    yield
