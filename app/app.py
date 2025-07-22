import pdb
import string
import random
import os
from flask import redirect, url_for, session, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import current_user, login_user, logout_user
from werkzeug.debug import console

from app import app, login
from app.controller.AccountController import account_bp
from app.controller.HomeController import index_bp
from app.dao import UserDao
from app.model.User import UserRole, UserType

app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(index_bp, url_prefix='/')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google_bp = make_google_blueprint(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ],
    redirect_url=None,
    reprompt_consent=True
)
app.register_blueprint(google_bp, url_prefix="/login")


@login.user_loader
def load_user(user_id):
    return UserDao.get_user_by_id(user_id)


@app.route("/abc")
def test():
    if not google.authorized:
        return '<a href="/login/google?prompt=select_account">Đăng nhập với Google</a>'
    # Nếu đã đăng nhập, hiển thị trang chính luôn
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Không lấy được thông tin người dùng", 400
    user_info = resp.json()

    email = user_info.get("email")
    username = email.split('@')[0]
    password = ''.join(random.choices(string.digits, k=8))
    return render_template("test.html", email=email, username=username, password=password)


@app.route("/login/google", methods=['GET', 'POST'])
def login_google():
    if not google.authorized:
        return redirect(url_for('google.login', prompt='select_account'))
    # Nếu đã đăng nhập, hiển thị trang chính luôn
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Không lấy được thông tin người dùng", 400
    user_info = resp.json()

    email = user_info.get("email")
    username = email.split('@')[0]
    check = UserDao.check_exists_email(email=email)
    print("===> Đang tạo user mới:")
    print("username:", username)
    print("email:", email)
    print("Check", check)

    if check == 1:
        user = UserDao.auth_user(identifier=email, password=None, user_type=UserType.GOOGLE)
        if user:
            login_user(user)
            return redirect(url_for('index.search_main'))
        else:
            return "Lỗi xác thực người dùng Google", 400
    else:
        # Tạo user mới với username trước @, password random 8 số, avatar mặc định
        password = ''.join(random.choices(string.digits, k=8))
        try:

            pdb.set_trace()
            UserDao.add_user(
                first_name='',
                last_name='',
                username=username,
                password=password,
                email=email,
                phone_number=None,
                avt_url='https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg',
                sex=None,
                date_of_birth=None,
                isActive=True,
                last_access=None,
                role=UserRole.USER,
                user_type=UserType.GOOGLE
            )
            pdb.set_trace()
        except Exception as e:
            print("Lỗi khi thêm user mới:", e)
            return "Lỗi tạo tài khoản Google", 500

        user = UserDao.auth_user(identifier=email, password=None, user_type=UserType.GOOGLE)
        if user:
            login_user(user)
            return redirect(url_for('index.search_main'))
        else:
            return "Lỗi tạo tài khoản Google", 500


@app.route("/logout")
def logout():
    logout_user()
    session.pop("google_oauth_token", None)
    session.clear()
    return redirect(url_for('index.search_main'))


if __name__ == "__main__":
    app.run(debug=True)