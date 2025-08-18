from flask import Blueprint, render_template
from flask import request
import app
from app.dao.BookDAO import find_all, paginate_book, find_by_id, search_book
from app.dao.BookGerneDAO import find_all as find_all_genre
from flask import Blueprint, request, redirect, url_for, flash, session
from app.dao.RequestDAO import RequestDAO
from app.dao.ActivityLogDAO import ActivityLogDAO
from flask_login import current_user

book_controller_bp = Blueprint('book_controller', __name__)

@book_controller_bp.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    if not current_user.is_authenticated:
        flash("Bạn cần đăng nhập để mượn sách!", "danger")
        return redirect(url_for('account.login'))

    user_id = current_user.user_id

    msg_request, status_request = RequestDAO.create_request(user_id, book_id)
    msg_log, status_activity_log = ActivityLogDAO.create_activity_log(user_id, book_id)

    if status_request == 201 and status_activity_log == 201:
        flash("Đã gửi yêu cầu mượn sách!", "success")
    else:
        # Hiển thị lỗi chi tiết từ DAO (nếu có)
        if status_request == 409 or status_activity_log != 409:
            flash("Trả đi mày!", "danger")

    return redirect(url_for('index.get_detail', bookId=book_id))


