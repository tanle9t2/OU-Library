from app import db
from app.authentication.login_required import admin_required
from app.dao.RequestDAO import find_all_waiting_request, accept_request, cancel_request
from app.model.Book import BookFormat
from flask import Blueprint, redirect, url_for
from flask import jsonify
from flask import render_template, request
from app.utils.helper import FORMAT_BOOK_TEXT
from app.model.Book import Book
from app.model.Publisher import Publisher
from app.dao.PublisherDAO import find_all as find_all_publisher

employee_bp = Blueprint('employee', __name__)


@employee_bp.route("/add-products")
def add_products_process():
    publishers = find_all_publisher()
    return render_template("employee/employeeAddProducts.html", publishers=publishers, formats=FORMAT_BOOK_TEXT)


@employee_bp.route("/handle-borrowing")
@admin_required
def handle_borrowing_request():
    all_query_params = dict(request.args)

    limit = int(all_query_params.pop('limit', 5))
    page = int(all_query_params.pop('page', 1))
    range_date = all_query_params.pop('date', None)
    order = all_query_params.pop('order', None)

    request_borrowing = find_all_waiting_request(page=page, limit=limit, date=range_date, order=order)

    return render_template("admin/adminHandleRequest.html",
                           nextPage=request_borrowing['current_page'] + 1,
                           prevPage=request_borrowing['current_page'] - 1,
                           request_borrowing=request_borrowing)


@employee_bp.route("/accept-request/<book_request_id>", methods=["POST"])
@admin_required
def handle_accept_request(book_request_id):
    accept_request(book_request_id)
    return redirect(url_for('employee.handle_borrowing_request'))


@employee_bp.route("/cancel-request/<book_request_id>", methods=["POST"])
@admin_required
def handle_cancel_request(book_request_id):
    note = request.form.get("note")
    cancel_request(book_request_id, note)
    return redirect(url_for('employee.handle_borrowing_request'))


@employee_bp.route('/update-book/<int:book_id>', methods=['POST'])
@admin_required
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
@admin_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404
    book.is_active = False
    db.session.commit()

    return jsonify({"success": True})


@employee_bp.route("/profile")
@admin_required
def employee_profile():
    return render_template("/employee/employeeProfile.html")
