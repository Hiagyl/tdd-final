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

