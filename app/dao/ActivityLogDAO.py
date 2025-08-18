from app.model.Book import Book
from app.model.ActivityLog import ActivityLog
from app import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class ActivityLogDAO:
    @staticmethod
    def create_activity_log(user_id: int, book_id: int, note: str = None):
        try:
            book = Book.query.filter_by(book_id=book_id).first()

            existing_activity_log = ActivityLog.query.filter_by(user_id=user_id, book_id=book_id).first()
            if existing_activity_log:
                return {"error": "Bạn đã mượn sách này trước đó, cần trả trước khi mượn lại."}, 409

            if book.borrowing >= book.quantity:
                return {"error": "Book is not available for borrowing"}, 400

            existing_activity_log = ActivityLog.query.filter_by(user_id=user_id, book_id=book_id).first()
            if existing_activity_log:
                return {"error": "You already requested this book"}, 409

            activity_log = ActivityLog(
                user_id=user_id,
                book_id=book_id,
                action="Muon",
                created_at=datetime.utcnow()
            )

            db.session.add(activity_log)
            db.session.commit()

            return activity_log.to_dict(), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500
