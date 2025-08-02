from datetime import datetime
from functools import wraps

from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request, render_template, url_for

from app.model.User import UserRole


def admin_required(f):
    @wraps(f)  # Sử dụng functools.wraps để preserve metadata
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('account.admin_login'))
        if current_user.user_role != UserRole.LIBRARIAN:
            return redirect(url_for('account.admin_login'))
        return f(*args, **kwargs)
    return wrap


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

# Thêm các view
admin.add_view(AdminConfig(name='Cấu hình', endpoint='config'))
admin.add_view(AdminProfile(name='Hồ sơ', endpoint='profile'))
admin.add_view(AdminLogout(name='Đăng xuất', endpoint='logout'))