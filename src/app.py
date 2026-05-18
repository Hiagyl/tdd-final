from flask import Flask, jsonify, request

# This acts as the In-Memory Data Storage (Global State)
books = []


def create_app():
    app = Flask(__name__)

    @app.route('/books', methods=['POST'])
    def add_book_endpoint():
        return jsonify({"message": "stub"}), 501

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
