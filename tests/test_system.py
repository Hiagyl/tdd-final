# tests/test_system.py
import pytest
from playwright.sync_api import expect

# The live_server fixture starts your Flask app automatically


@pytest.mark.usefixtures('live_server')
def test_user_story_1_add_book(page, live_server):
    """
    User Story 1: As a reader, I want to add a new book with a title and author.
    """
    page.goto(live_server.url())

    # Fill out the form
    page.fill("#title", "1984")
    page.fill("#author", "George Orwell")
    page.click("#add-book-btn")

    # Check if the book appears in the list
    expect(page.locator("#book-list")).to_contain_text("1984")


@pytest.mark.usefixtures('live_server')
def test_user_story_2_view_list(page, live_server):
    """
    User Story 2: As a librarian, I want to view a list of all saved books.
    """
    page.goto(live_server.url())

    # The list should exist even if empty
    expect(page.locator("#book-list")).to_be_visible()


@pytest.mark.usefixtures('live_server')
def test_user_story_3_persistent_content_load(page, live_server):
    """
    User Story 3: As a returning user, I want the system to automatically load 
    and display my previously saved book collection upon opening the application.
    """
    # Step 1: Seed a book into the database session first
    page.goto(live_server.url())
    page.fill("#title", "Brave New World")
    page.fill("#author", "Aldous Huxley")
    page.click("#add-book-btn")
    expect(page.locator("#book-list")).to_contain_text("Brave New World")

    # Step 2: Reload/Revisit the page to simulate a returning user session
    page.goto(live_server.url())

    # Step 3: Verify the frontend script successfully fetches and maps the persistent data
    expect(page.locator("#book-list")).to_contain_text("Brave New World")


@pytest.mark.usefixtures('live_server')
def test_user_story_3_remove_book(page, live_server):
    page.goto(live_server.url())

    # Pre-seed a book entry
    page.fill("#title", "Dune")
    page.fill("#author", "Frank Herbert")
    page.click("#add-book-btn")

    # 🎯 FIX: Locate the specific list element for Dune, then find its delete button
    dune_item = page.locator("#book-list li", has_text="Dune")
    dune_item.locator(".delete-btn").click()

    # Assert entry is purged from visible UI list
    expect(page.locator("#book-list")).not_to_contain_text("Dune")
