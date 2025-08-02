from app import db
from app.authentication.login_required import employee_sale_required, employee_manager_warehouse_required, \
    employee_manager_required, employee_required, employee_manager_required_api
from app.model.Book import BookFormat
from flask import Blueprint
from flask import jsonify
from flask import render_template, redirect, url_for, request
from app.utils.helper import FORMAT_BOOK_TEXT
from app.model.BookGerne import BookGerne
from app.model.Book import Book
from app.model.Publisher import Publisher
from app.dao.PublisherDAO import find_all as find_all_publisher

employee_bp = Blueprint('employee', __name__)



@employee_bp.route("/add-products")
@employee_manager_required
def add_products_process():
    publishers = find_all_publisher()
    return render_template("employee/employeeAddProducts.html", publishers=publishers, formats=FORMAT_BOOK_TEXT)


@employee_bp.route('/update-book/<int:book_id>', methods=['POST'])
@employee_manager_required
def update_book(book_id):
    try:
        updated_data = request.get_json()
        print("Received data:", updated_data)
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'success': False, 'message': 'Book not found'}), 404

        book.title = updated_data.get('title', book.title)
        book.author = updated_data.get('author', book.author)
        book.book_gerne_id = updated_data.get('gerne', book.book_gerne_id)

        barcode = updated_data.get('barcode')
        if barcode:
            existing_book = Book.query.filter_by(barcode=barcode).first()
            if existing_book and existing_book.book_id != book.book_id:
                return jsonify({'success': False, 'message': f"Barcode '{barcode}' already exists"}), 400
            book.barcode = barcode

        publisher_name = updated_data.get('publisher')
        if publisher_name:
            publisher = Publisher.query.filter_by(publisher_name=publisher_name).first()
            if publisher:
                book.publisher_id = publisher.publisher_id
            else:
                return jsonify({'success': False, 'message': f"Publisher '{publisher_name}' not found"}), 400

        format_value = updated_data.get('format')
        if format_value:
            try:
                if isinstance(format_value, int):  # Nếu là số
                    book.format = BookFormat(format_value)  # Chuyển trực tiếp từ số sang Enum
                elif format_value.startswith('BookFormat.'):  # Nếu là chuỗi dạng 'BookFormat.BIA_MEM'
                    book.format = BookFormat[format_value.split('BookFormat.')[1]]
                else:  # Nếu là chuỗi tên Enum như 'BIA_MEM'
                    book.format = BookFormat[format_value]
            except KeyError:
                return jsonify({'success': False, 'message': f"Invalid format value: {format_value}"}), 400

        book.price = updated_data.get('price', book.price)
        book.num_page = updated_data.get('num_page', book.num_page)
        book.weight = updated_data.get('weight', book.weight)
        # book.format = updated_data.get('format', book.format)
        book.dimension = updated_data.get('dimension', book.dimension)

        db.session.commit()

        return jsonify({'success': True, 'updated': updated_data})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@employee_bp.route('/delete-book/<int:book_id>', methods=['POST'])
@employee_manager_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404
    book.is_active = False
    db.session.commit()

    return jsonify({"success": True})


@employee_bp.route("/profile")
@employee_required
def employee_profile():
    return render_template("/employee/employeeProfile.html")
