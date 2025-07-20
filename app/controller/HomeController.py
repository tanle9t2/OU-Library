from flask import Blueprint
from flask import render_template, request, redirect, url_for, session

from app.dao.BookDAO import find_all, paginate_book, find_by_id, search_book
from app.dao.BookGerneDAO import find_all as find_all_genre
index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def search_main():
    all_query_params = dict(request.args)

    keyword = all_query_params.pop('keyword', None)
    order = all_query_params.pop('order', 'id')
    limit = int(all_query_params.pop('limit', 12))
    page = int(all_query_params.pop('page', 1))

    book = search_book(keyword=keyword, page=page, order=order, limit=limit)
    genres = find_all_genre()

    return render_template("search.html"
                           , keyword=keyword
                           , genres=genres
                           , order=order
                           , limit=limit
                           , params=all_query_params
                           , pagination=book)
