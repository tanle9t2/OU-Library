from app.model.Book import Book
from app.model.ActivityLog import ActivityLog
from app import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def create_activity_log(user_id: int, book_id: int, action: str = None):
    try:
        activity_log = ActivityLog(
            user_id=user_id,
            book_id=book_id,
            action=action,
            created_at=datetime.now()
        )

        db.session.add(activity_log)
        db.session.commit()

        return activity_log.to_dict(), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500
