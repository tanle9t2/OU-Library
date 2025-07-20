from flask import Blueprint, render_template
from flask import request
import app
from app.dao.BookDAO import find_all, paginate_book, find_by_id, search_book
from app.dao.BookGerneDAO import find_all as find_all_genre

book_controller_bp = Blueprint('book_controller', __name__)



