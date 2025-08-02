from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Double, DATETIME, DATE, Enum
from app import db, app
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum


class Status(PythonEnum):
    WAIT = "Doi"
    ACCEPT = "Dong y"
    CANCEL = "Huy"


class Request(db.Model):
    __tablename__ = 'book_request'
    book_request_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    status = Column(Enum(Status), default=Status.WAIT)
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False)
    note = Column(String)

    user = relationship('User', uselist=False)
    book = relationship('Book', uselist=False)

    def to_dict(self):
        return {
            "book_request_id": self.book_request_id,
            "user_id": self.user_id,
            "status": self.status,
            "book_id": self.book_id,
            "note": self.note
        }

    def to_dto(self):
        return {
            "book_request_id": self.book_request_id,
            "user_id": self.user_id,
            "status": self.status,
            "book_id": self.book_id,
            "note": self.note
        }

    def __str__(self):
        pass

    # def increase_book(self, quantity):
    #     self.quantity += quantity
    #
    # def decrease_book(self, quantity):
    #     if self.quantity < quantity:
    #         return False
    #     self.quantity -= quantity
    #     return True
