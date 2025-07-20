from app import app, login
from app.controller.AccountController import account_bp
from app.controller.HomeController import index_bp
from app.dao.UserDao import get_user_by_id

from flask_login import current_user

app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(index_bp, url_prefix='/')

@login.user_loader
def get_by_id(user_id):
    return get_user_by_id(user_id)

from flask import Flask, redirect, url_for, session, render_template
from flask_dance.contrib.google import make_google_blueprint, google
import os
from app import app

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

@app.route("/")
def index():
    if not google.authorized:
        return '<a href="/login/google?prompt=select_account">Đăng nhập với Google</a>'
    # Nếu đã đăng nhập, hiển thị trang chính luôn
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Không lấy được thông tin người dùng", 400
    user_info = resp.json()
    name = user_info.get("name")
    email = user_info.get("email")
    return render_template("home.html", name=name, email=email)


@app.route("/logout")
def logout():
    session.pop("google_oauth_token", None)  # Xóa token Google OAuth
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
