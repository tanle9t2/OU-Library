from flask import Blueprint
from flask import render_template, request, redirect, url_for, session

from app.dao.BookDAO import find_all, paginate_book, find_by_id, search_book, count_book_sell
from app.dao.BookGerneDAO import find_all as find_all_genre
from app.utils.helper import FORMAT_BOOK_TEXT

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
