from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Double, DATETIME, DATE, Enum
from app import db, app
from sqlalchemy.orm import relationship
from app.model.BookGerne import BookGerne
from app.model.Publisher import Publisher

from enum import Enum as PythonEnum

from app.utils.helper import FORMAT_BOOK_TEXT


class BookFormat(PythonEnum):
    BIA_CUNG = "Bìa Cứng"
    BIA_MEM = "Bìa Mềm"


class Book(db.Model):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    quantity = Column(Integer, default=0)
    price = Column(Double)
    description = Column(String)
    release_date = Column(DATE)
    created_at = Column(DATETIME, default=datetime.now())
    num_page = Column(Integer)
    dimension = Column(String)
    weight = Column(Double)
    barcode = Column(String)
    format = Column(String)
    publisher_id = Column(Integer, ForeignKey('publisher.publisher_id'), nullable=False)
    book_gerne_id = Column(Integer, ForeignKey('book_gerne.book_gerne_id'))
    image_url = Column(String)
    book_gerne = db.relationship('BookGerne', back_populates='books', lazy=True)
    publisher_info = db.relationship('Publisher', back_populates='publisher_books_relation', uselist=False,
                                     foreign_keys=[publisher_id], lazy=True, cascade='all')
    borrowing = Column(Integer, default=0)

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "author": self.author,
            "title": self.title,
            'created_at': self.created_at,
            'release_date': self.release_date,
            "quantity": self.quantity,
            "price": self.price,
            "description": self.description,
            "book_gerne_id": self.book_gerne_id,
            "page_number": self.num_page,
            "weight": self.weight,
            "image_url": self.image_url,
            'format': self.format,
            "publisher": self.publisher_info.to_dict() if self.publisher_info else None,
            'book_gerne': self.book_gerne.to_dict(),
            'borrowing': self.borrowing,
        }

    def to_dto(self):
        return {
            "book_id": self.book_id,
            "author": self.author,
            "title": self.title,
            'created_at': self.created_at,
            'release_date': self.release_date,
            "quantity": self.quantity,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "book_gerne": self.book_gerne.to_dto(),
            "page_number": self.num_page,
            "weight": self.weight,
            'format': self.format,
            "publisher": "Kim đồng",
            "borrowing": self.borrowing,
        }

    def __str__(self):
        pass

    def increase_book(self, quantity):
        self.quantity += quantity

    def decrease_book(self, quantity):
        if self.quantity < quantity:
            return False
        self.quantity -= quantity
        return True
