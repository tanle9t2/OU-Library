from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Double, DATETIME, DATE, Enum
from app import db, app
from sqlalchemy.orm import relationship


class ActivityLog(db.Model):
    __tablename__ = 'activity_log'
    activity_log_id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String)
    created_at = Column(DATETIME)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False)

    user = relationship('User', uselist=False)
    book = relationship('Book', uselist=False)

    def to_dict(self):
        return {
            "activity_log_id": self.activity_log_id,
            "action": self.action,
            "created_at": self.created_at,
            "user_id": self.user_id,
            "full_name": self.user.full_name,
            "book_id": self.book_id,
            "book_title": self.book.title
        }

    def to_dto(self):
        return {
            "activity_log_id": self.activity_log_id,
            "action": self.action,
            "created_at": self.created_at,
            "user_id": self.user_id,
            "full_name": self.user.full_name,
            "book_id": self.book_id,
            "book_title": self.book.title
        }

    def __str__(self):
        pass
