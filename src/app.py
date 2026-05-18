# src/app.py
from flask import Flask, jsonify, request
from src.logic import BookCatalog

# Global persistence reference layer for runtime state
catalog = BookCatalog()
# Kept as a reference shortcut to satisfy conftest.py clearing rules
books = catalog.books


def create_app():
    app = Flask(__name__)

    @app.route('/books', methods=['GET', 'POST'])
    def handle_books():
        if request.method == 'POST':
            data = request.get_json() or {}
            title = data.get('title')
            author = data.get('author')

            # Use logic validation layer directly
            try:
                new_book = catalog.add_book(title, author)
                return jsonify(new_book), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        # GET method processing
        return jsonify(catalog.books), 200

    @app.route('/books/<int:index>', methods=['PUT', 'DELETE'])
    def handle_single_book(index):
        if request.method == 'PUT':
            data = request.get_json() or {}
            title = data.get('title')
            author = data.get('author')

            # Process minimum business validation updates inline
            if not title or not title.strip() or not author or not author.strip():
                return jsonify({"error": "Title and Author cannot be empty"}), 400

            if index < 0 or index >= len(catalog.books):
                return jsonify({"error": "Book index mapping not found"}), 404

            catalog.books[index] = {
                "title": title.strip(), "author": author.strip()}
            return jsonify({"message": "Book updated successfully", "title": title.strip()}), 200

        if request.method == 'DELETE':
            try:
                catalog.remove_book_by_index(index)
                return jsonify({"message": "Book deleted successfully"}), 200
            except IndexError:
                return jsonify({"error": "Book index mapping not found"}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
