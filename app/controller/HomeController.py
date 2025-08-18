from flask import Blueprint
from flask import render_template, request, redirect, url_for, session

from app.dao.BookDAO import find_all, paginate_book, find_by_id, search_book, count_book_sell
from app.dao.BookGerneDAO import find_all as find_all_genre
from app.dao.PublisherDAO import find_all as find_all_publisher
from app.utils.helper import FORMAT_BOOK_TEXT
from app.model.Request import Request
from flask_login import login_user, logout_user, current_user

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def search_main():
    all_query_params = dict(request.args)

    keyword = all_query_params.pop('keyword', None)
    order = all_query_params.pop('order', 'id')
    limit = int(all_query_params.pop('limit', 12))
    page = int(all_query_params.pop('page', 1))
    genre_params = all_query_params.pop('genre', None)
    publisher_params = all_query_params.pop('publisher', None)

    if genre_params:
        genre_params = list(map(int, genre_params.split(',')))

    if publisher_params:
        publisher_params = list(map(int, publisher_params.split(',')))

    book = search_book(keyword=keyword, genres=genre_params, publishers=publisher_params,
                       page=page, order=order, limit=limit)
    genres = find_all_genre()
    publishers = find_all_publisher()

    return render_template("search.html"
                           , keyword=keyword
                           , genres=genres
                           , genre_params=genre_params
                           , publisher_params=publisher_params
                           , publishers=publishers
                           , order=order
                           , limit=limit
                           , params=all_query_params
                           , pagination=book)


@index_bp.route('/detail')
def get_detail():
    book_id = request.args.get('bookId', type=int)
    book = find_by_id(book_id)
    books = search_book(gerne_id=book.book_gerne_id, limit=12)['books']
    # sold_book = count_book_sell(book_id)
    sold_book = 1;
    detail_book = {
        "Mã sản phẩm": book.book_id,
        "Tác giả": book.author,
        "Trọng lượng (gr)": book.weight,
        "Kích thước bao bì": book.dimension,
        "Số trang": book.num_page,
        "Hình thức": book.format,
    }

    return render_template("book-detail.html", book=book.to_dict()
                           , sold_book=sold_book
                           , detail_book=detail_book
                           , books=books)



@index_bp.route("/history")
def history():
    requests = Request.query.filter_by(user_id=current_user.user_id).all()
    return render_template("history.html", requests=requests)