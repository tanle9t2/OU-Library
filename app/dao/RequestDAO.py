from app.model.Book import Book
from app.model.Request import Request, Status
from app import db
from sqlalchemy.exc import SQLAlchemyError

class RequestDAO:
    @staticmethod
    def create_request(user_id: int, book_id: int, note: str = None):
        try:
            book = Book.query.filter_by(book_id=book_id).first()

            existing_request = Request.query.filter_by(user_id=user_id, book_id=book_id).first()
            if existing_request:
                return {"error": "Bạn đã gửi yêu cầu mượn sách này trước đó."}, 409

            if book.borrowing >= book.quantity:
                return {"error": "Book is not available for borrowing"}, 400

            existing_request = Request.query.filter_by(user_id=user_id, book_id=book_id).first()
            if existing_request:
                return {"error": "You already requested this book"}, 409

            request = Request(
                user_id=user_id,
                book_id=book_id,
                status=Status.WAIT,
                note=note
            )

            book.borrowing += 1
            book.quantity -= 1

            db.session.add(request)
            db.session.commit()

            return request.to_dict(), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500
