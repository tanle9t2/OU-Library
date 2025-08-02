import random
import threading

from app import login
from sendgrid.helpers.mail import Mail, Email, To, Content
from sendgrid import SendGridAPIClient

from app.dao.UserDao import is_valid_email
from app.model.User import UserRole
from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from flask import Blueprint
from app.dao import UserDao

account_bp = Blueprint('account', __name__)

def send_email_async(message):
    try:
        sg = SendGridAPIClient(api_key="12")
        sg.send(message)
    except Exception as e:
        print(f"Lỗi khi gửi email: {str(e)}")


@account_bp.route("/login", methods=['GET', 'POST'])
def login_process():
    err_msg = ''
    if request.method == 'POST':
        identifier = request.form.get('username')
        password = request.form.get('password')

        roles = [UserRole.USER, UserRole.LIBRARIAN]

        u = None
        for role in roles:
            u = UserDao.auth_user(identifier=identifier, password=password, role=role)
            if u:
                break
        if u:
            login_user(u)

            return redirect(url_for('index.search_main'))
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!"

    return render_template("login.html", err_msg=err_msg)


@account_bp.route("/verify", methods=['GET', 'POST'])
def verify_email():
    return redirect(url_for('account.register_process'))

@account_bp.route("/register", methods=['get', 'post'])
def register_process():
    err_msg = ''
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        if not username:
            err_msg = "Vui lòng nhập tên người dùng!"
        elif not password:
            err_msg = "Vui lòng nhập mật khẩu!"
        elif not confirm:
            err_msg = "Vui lòng xác nhận mật khẩu!"
        elif not phone_number:
            err_msg = "Vui lòng nhập số điện thoại!"
        elif not email:
            err_msg = "Vui lòng nhập số email"
        elif len(phone_number) > 10:
            err_msg = "Số điện thoại quá dài. Vui lòng nhập lại."
        elif password != confirm:
            err_msg = "Mật khẩu không khớp!"
        else:
            if len(phone_number) > 10:
                err_msg = "Số điện thoại quá dài. Vui lòng nhập lại."
                return render_template('register.html', err_msg=err_msg)

            if password == confirm:
                check =  UserDao.check_exists(username=username, email=email, phone_number=phone_number)
                if check == 1:
                    err_msg = 'Tên người dùng hoặc email hoặc SĐT đã tồn tại!'
                else:
                    data = request.form.copy()
                    del data['confirm']
                    avt_url = request.files.get('avt_url')
                    optional_fields = ['sex', 'phone_number', 'date_of_birth', 'isActive', 'last_access']
                    for field in optional_fields:
                        data[field] = data.get(field, None)
                    UserDao.add_user(
                        first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        username=username,
                        password=password,
                        email=email,
                        phone_number=phone_number,
                        avt_url=avt_url,
                        sex=data.get('sex', True),
                        date_of_birth=data.get('date_of_birth'),
                        isActive=data.get('isActive'),
                        last_access=data.get('last_access')
                    )
                    return redirect(url_for('account.login_process'))
            else:
                err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@account_bp.route("/logout")
def logout_process():
    logout_user()
    return redirect('/')



@account_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    err_msg = ''
    if request.method == 'POST':
        identifier = request.form.get('username')
        password = request.form.get('password')

        user = UserDao.auth_user(identifier=identifier, password=password)
        if user:
            if user.user_role == UserRole.LIBRARIAN:
                login_user(user=user)
                return redirect('/admin/')
            else:
                err_msg = "Vai trò không hợp lệ!"
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!"

    return render_template('admin-login.html', err_msg=err_msg)


@account_bp.route("/admin-logout")
def admin_logout():
    logout_user()
    return redirect(url_for('account.admin_login'))

