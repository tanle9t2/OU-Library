from app import db



class BookGerne(db.Model):
    __tablename__ = 'book_gerne'
    book_gerne_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    books = db.relationship('Book', back_populates='book_gerne', lazy=True)

    def __init__(self, name, lft, rgt):
        self.name = name
        self.lft = lft
        self.rgt = rgt

    def to_dict(self):
        return {
            'book_type_id': self.book_gerne_id,
            'name': self.name,
        }

    def to_dto(self):
        return {
            'book_gerne_id': self.book_gerne_id,
            'name': self.name,
        }
