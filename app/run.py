import pdb
import string
import random
import os

from firebase_admin import messaging
from flask import redirect, url_for, session, render_template, request, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import current_user, login_user, logout_user

from werkzeug.middleware.proxy_fix import ProxyFix
from app import db
from app import app, login
from app.controller.AccountController import account_bp
from app.controller.HomeController import index_bp
from app.dao import UserDao
from app.model.User import UserRole, UserType

# QUAN TRỌNG: Cấu hình để Flask hiểu ngrok proxy
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
    x_prefix=1
)

app.config['PREFERRED_URL_SCHEME'] = 'https'

app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(index_bp, url_prefix='/')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'

google_bp = make_google_blueprint(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ],
    redirect_url="/account/google/login",
    reprompt_consent=True
)

app.register_blueprint(google_bp, url_prefix="/login")


@login.user_loader
def load_user(user_id):
    return UserDao.get_user_by_id(user_id)


@app.route("/monitor")
def monitor():
    return render_template("monitor.html")


@app.route("/account/google/login")
def abc_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Không lấy được thông tin người dùng", 400

    user_info = resp.json()
    email = user_info.get("email")
    username = email.split('@')[0]
    password = ''.join(random.choices(string.digits, k=8))
    first_name = user_info.get("given_name", "")
    last_name = user_info.get("family_name", "")
    avt_url = user_info.get(
        "picture") or 'https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg'

    check = UserDao.check_exists_email(email=email)

    if check == 1:
        user = UserDao.get_user_by_email(email)
        if user and user.user_type != UserType.GOOGLE:
            user.user_type = UserType.GOOGLE
            user.avt_url = avt_url
            db.session.commit()
        user = UserDao.auth_user(identifier=email, user_type=UserType.GOOGLE)
    else:
        # Tạo user mới
        UserDao.add_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            phone_number=None,
            avt_url=avt_url,
            sex=None,
            date_of_birth=None,
            isActive=True,
            last_access=None,
            role=UserRole.USER,
            user_type=UserType.GOOGLE
        )
        user = UserDao.auth_user(identifier=email, user_type=UserType.GOOGLE)

    if user:
        login_user(user)
        return redirect(url_for('index.search_main'))
    else:
        return "Lỗi xác thực", 500


@app.route("/logout")
def logout():
    logout_user()
    session.pop("google_oauth_token", None)
    session.clear()
    return redirect(url_for('index.search_main'))


def send_notification_to_user(user_id,title,body):
    topic = f"user_{user_id}"
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        topic=topic
    )
    response = messaging.send(message)
    return response


@app.route("/subscribe_topic", methods=["POST"])
def subscribe_topic():
    data = request.json
    user_id = data.get("userId")
    token = data.get("token")

    if not user_id or not token:
        return jsonify({"error": "Missing userId or token"}), 400

    topic = f"user_{user_id}"  # unique topic per user

    try:
        response = messaging.subscribe_to_topic([token], topic)
        print("Subscribe response:", response)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
