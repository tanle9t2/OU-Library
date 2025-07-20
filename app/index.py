from app import app
from app.controller.BookController import book_controller_bp

app.register_blueprint(book_controller_bp, url_prefix='/search')


if __name__ == "__main__":
    app.run(debug=True)
