from flask import Blueprint, render_template
from flask import request
import app
from app.dao.BookDAO import find_all, paginate_book, find_by_id, search_book
from app.dao.BookGerneDAO import find_all as find_all_genre

book_controller_bp = Blueprint('book_controller', __name__)


@book_controller_bp.route('/')
def search_main():
    all_query_params = dict(request.args)

    keyword = all_query_params.pop('keyword', None)
    order = all_query_params.pop('order', 'id')
    limit = int(all_query_params.pop('limit', 12))
    page = int(all_query_params.pop('page', 1))

    book = search_book(keyword=keyword, page=page, order=order,limit=limit)
    genres = find_all_genre()

    return render_template("search.html"
                           , keyword=keyword
                           , genres=genres
                           , order=order
                           , limit=limit
                           , params=all_query_params
                           , pagination=book)


@book_controller_bp.route('/book')
def get_books():
    return uploadImage()
