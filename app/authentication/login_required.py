from functools import wraps

from flask import redirect, url_for
from flask_login import current_user

from app.model.User import UserRole

def customer_no_user_required(f):
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('account.logout_process'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def login_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.USER, UserRole.LIBRARIAN]:
            return redirect(url_for('account.login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

def admin_required(f):
    @wraps(f)  # Sử dụng functools.wraps để preserve metadata
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('account.admin_login'))
        if current_user.user_role != UserRole.LIBRARIAN:
            return redirect(url_for('account.admin_login'))
        return f(*args, **kwargs)
    return wrap


