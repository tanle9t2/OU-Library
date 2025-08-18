from firebase_admin import messaging

from app import app, login
from app.controller.AccountController import account_bp
from app.controller.HomeController import index_bp
from app.controller.EmployeeController import employee_bp
from app.dao.UserDao import get_user_by_id

from flask import Flask, redirect, url_for, session, render_template, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
import os
from app import app
from flask_login import current_user

app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(employee_bp, url_prefix='/employee')

@login.user_loader
def get_by_id(user_id):
    return get_user_by_id(user_id)


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


@app.route("/logout")
def logout():
    session.pop("google_oauth_token", None)  # Xóa token Google OAuth
    session.clear()
    return redirect(url_for("index"))
from app.controller.BookController import book_controller_bp

app.register_blueprint(book_controller_bp, url_prefix='/search')


if __name__ == "__main__":
    from app.admin import *

    app.run(debug=True)
