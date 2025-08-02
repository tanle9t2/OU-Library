from datetime import datetime
from functools import wraps
from sqlalchemy import or_, func, case, desc
from flask import jsonify

from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request, render_template, url_for

from app.authentication.login_required import admin_required
from app.model.Book import Book, BookFormat
from app.model.BookGerne import BookGerne
from app.model.Publisher import Publisher
from app.model.User import UserRole

class AdminHome(AdminIndexView):
    @expose("/")
    @admin_required
    def index(self):
        return self.render("/admin/adminHome.html")


class AdminConfig(BaseView):  # Sử dụng BaseView thay vì ModelView
    @expose("/", methods=("GET", "POST"))
    @admin_required
    def index(self):  # Phải là index() cho BaseView
        # Thay thế config() bằng logic cấu hình thực tế
        config_data = {
            'site_name': 'Library Management',
            'max_books_per_user': 5,
            'loan_duration_days': 14
        }
        return self.render("/admin/adminConfig.html", config=config_data)


class AdminProfile(BaseView):  # Sử dụng BaseView thay vì ModelView
    @expose("/", methods=("GET", "POST"))
    @admin_required
    def index(self):  # Phải là index() cho BaseView
        return self.render("/admin/adminProfile.html", user=current_user)


# Logout view
class AdminLogout(BaseView):
    @expose("/")
    @admin_required
    def index(self):
        logout_user()
        return redirect(url_for('account.admin_login'))


# Khởi tạo admin
admin = Admin(
    app=app,
    name='Library Admin',
    index_view=AdminHome(),
    template_mode='bootstrap4'
)

@app.route("/api/gernes", methods=["GET"])
def get_gernes():
    gernes = db.session.query(BookGerne.book_gerne_id, BookGerne.name).all()
    return jsonify([{"id": gerne.book_gerne_id, "name": gerne.name} for gerne in gernes])


@app.route('/api/formats', methods=['GET'])
def get_formats():
    formats = [{"id": format.value, "name": f"BookFormat.{format.name}"} for format in BookFormat]
    return jsonify(formats)

def book_management(gerne_id=None, kw=None, price_start=None, price_end=None):
    query = db.session.query(
        Book.book_id,
        Book.title,
        BookGerne.name.label("gerne_name"),
        Book.author,
        Publisher.publisher_name.label("publisher_name"),
        Book.price,
        Book.barcode,
        Book.num_page,
        Book.weight,
        Book.format,
        Book.dimension,
    ).outerjoin(BookGerne, BookGerne.book_gerne_id == Book.book_gerne_id) \
        .outerjoin(Publisher, Publisher.publisher_id == Book.publisher_id) \
        .group_by(Book.book_id, Book.title, BookGerne.name)

    if gerne_id is not None:
        query = query.filter(Book.book_gerne_id == gerne_id)

    if kw:
        keyword = f"%{kw}%"  # Chuẩn bị mẫu tìm kiếm
        query = query.filter(
            or_(
                Book.title.ilike(keyword),  # Tìm trong tiêu đề
                BookGerne.name.ilike(keyword),  # Tìm trong tên thể loại
                Book.author.ilike(keyword),  # Tìm trong tác giả
                Publisher.publisher_name.ilike(keyword)  # Tìm trong nhà xuất bản
            )
        )

    if price_start is not None:
        query = query.filter(Book.price >= price_start)

    if price_end is not None:
        query = query.filter(Book.price <= price_end)

    query = query.order_by(desc(Book.created_at))

    return query.all()

# Thêm các view
admin.add_view(AdminConfig(name='Cấu hình', endpoint='config'))
admin.add_view(AdminProfile(name='Hồ sơ', endpoint='profile'))
admin.add_view(AdminLogout(name='Đăng xuất', endpoint='logout'))