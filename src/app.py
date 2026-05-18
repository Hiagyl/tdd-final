# src/app.py
import os
from flask import Flask, jsonify, request, render_template
from src.logic import BookCatalog

# 🎯 FIX: Instantiate and expose catalog metrics globally so conftest.py can read them
catalog = BookCatalog()
books = catalog.books


def create_app():
    # Configure precise folder paths to ensure template finding works across fixtures
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, "templates")

    app = Flask(__name__, template_folder=template_dir)

    # Serve the user interface at the root URL so Playwright can find your HTML
    @app.route('/')
    def index():
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

        return jsonify(catalog.books), 200

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
