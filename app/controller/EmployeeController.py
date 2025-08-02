import math

from app import db, app
from app.admin import book_management
from app.authentication.login_required import admin_required
from app.model.Book import BookFormat
from flask import Blueprint
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
                    if format_value == 1:
                        book.format = "Bìa Cứng"
                    else:
                        book.format = "Bìa Mềm"
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


@employee_bp.route("/book-manager")
@admin_required
def book_manager():
    gerne_id = request.args.get('gerne_id', type=int)
    kw = request.args.get('kw')
    price_start = request.args.get('price_start', type=float)
    price_end = request.args.get('price_end', type=float)

    if gerne_id == 1:
        stats = book_management(kw=kw, price_start=price_start, price_end=price_end)
    else:
        stats = book_management(gerne_id, kw=kw, price_start=price_start, price_end=price_end)
    page = int(request.args.get('page', 1))
    page_size = app.config['BOOK_PAGE_SIZE']
    total = len(stats)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]

    # Render template
    return render_template(
        "/employee/employeeBookManager.html",
        stats=paginated_stats, full_stats=stats, kw=kw, price_start=price_start, price_end=price_end,
        books={
            'current_page': page,
            'total_page': math.ceil(total / page_size),
            'pages': range(1, math.ceil(total / page_size) + 1),
        }
    )
