import pdb

from sqlalchemy import text

import app.dao.BookDAO
from app import db

from app.model.BookGerne import BookGerne
import json


def find_by_id(book_gerne_id):
    return BookGerne.query.get(book_gerne_id)

def find_all():
    return BookGerne.query.all()
