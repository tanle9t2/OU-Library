import pdb

from flask import request, Blueprint, jsonify
from app import app
from app.dao.BookGerneDAO import find_all
book_gerne_rest_bp = Blueprint('book_gerne_rest', __name__)


@book_gerne_rest_bp.route('/all', methods=['GET'])
def get_all_gerne():
    genres = find_all()
    genres_data = [genre.to_dto() for genre in genres]

    return jsonify({
        "message": "SUCCESS",
        "status": 200,
        'data': genres_data
    })

@book_gerne_rest_bp.route('/<book_gerne_id>/attributes', methods=['GET'])
def get_attributes(book_gerne_id):
    attributes = find_all_extend_attribute(book_gerne_id)
    print('test',attributes)
    return jsonify({
        "message": "SUCCESS",
        "status": 200,
        'data': [attribute.to_dict() for attribute in attributes]
    })
