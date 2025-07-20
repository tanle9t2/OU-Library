from sqlalchemy import desc, asc, or_
from sqlalchemy.sql import text

from app.model.Book import Book
from app.model.BookGerne import BookGerne
from app import app, db
import math


def find_by_id(id):
    return Book.query.get(id)


def find_by_gerne(gerne_id):
    query = Book.query
    query = query.join(BookGerne)
    query = query.filter(BookGerne.book_gerne_id == gerne_id)
    return query.all()


def paginate_book(page=1, limit=app.config['PAGE_SIZE']):
    page_size = limit
    start = (page - 1) * page_size
    end = start + page_size
    total = Book.query.count()
    total_page = math.ceil(total / page_size)
    books = Book.query.slice(start, end).all()

    return {
        'total_book': total,
        'current_page': page,
        'pages': total_page,
        'books': books
    }


def find_all(page=1):
    return Book.query.all()


def countBook():
    return Book.query.count()


def count_book_sell(book_id):
    query = text(
        """
               select sum(od.quantity) as sold from (
                       select * from order_detail od
                       where od.order_id not in (select order_id from order_cancellation)
                   ) as od , book b
                   where od.book_id = b.book_id
                   and b.book_id = :book 
           """)
    result = db.session.execute(query, {'book': book_id}).fetchone()
    return result.sold if result.sold else 0


def search_book(keyword=None, order=None, direction=None, gerne_id=None, limit=None, page=1):
    query = Book.query
    if keyword:
        query = query.filter(
            or_(
                Book.title.contains(keyword),
                Book.author.contains(keyword),
                Book.description.contains(keyword),
            )
        )

    if order:
        if order == 'latest':
            query = query.order_by(desc(getattr(Book, "created_at")))
        elif order == 'oldest':
            query = query.order_by(asc(getattr(Book, "created_at")))
    if gerne_id:
        query = query.filter(Book.book_gerne_id == gerne_id)

    start = (page - 1) * limit
    end = start + limit
    query_count = query
    total = query_count.count()
    total_page = math.ceil(total / limit)
    query = query.slice(start, end)
    books = query.all()

    return {
        'total_book': total,
        'current_page': page,
        'pages': total_page,
        'books': books
    }
