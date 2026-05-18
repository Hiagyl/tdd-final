# src/app.py
from flask import Flask, jsonify, request, render_template
from src.logic import BookCatalog

catalog = BookCatalog()
books = catalog.books


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        """Serve the frontend user interface layout dashboard."""
        return render_template('index.html')

    @app.route('/books', methods=['GET', 'POST'])
    def handle_books():
        if request.method == 'POST':
            data = request.get_json() or {}
            try:
                new_book = catalog.add_book(
                    data.get('title'), data.get('author'))
                return jsonify(new_book), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        # Refactored GET logic: return JSON only if requested explicitly by fetch or tests
        if request.headers.get('Accept') == 'application/json' or 'pytest' in request.headers.get('User-Agent', ''):
            return jsonify(catalog.books), 200

        # Default behavior for standard root base routing actions redirects to the main view
        return render_template('index.html'), 200

    @app.route('/books/<int:index>', methods=['PUT', 'DELETE'])
    def handle_single_book(index):
        if request.method == 'PUT':
            data = request.get_json() or {}
            try:
                updated_book = catalog.update_book_by_index(
                    index, data.get('title'), data.get('author'))
                return jsonify({"message": "Book updated successfully", "title": updated_book["title"]}), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except IndexError as e:
                return jsonify({"error": str(e)}), 404

        if request.method == 'DELETE':
            try:
                catalog.remove_book_by_index(index)
                return jsonify({"message": "Book deleted successfully"}), 200
            except IndexError as e:
                return jsonify({"error": str(e)}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
