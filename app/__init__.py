from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from urllib.parse import quote
from dotenv import dotenv_values, load_dotenv
import cloudinary
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
import firebase_admin
from firebase_admin import credentials, messaging
from app.utils.helper import format_currency_filter, format_datetime_filter, format_date_VN

app = Flask(__name__)
load_dotenv()

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
app.config['PREFERRED_URL_SCHEME'] = 'https'
#
# cred = credentials.Certificate(os.getenv("FIREBASE_PATH"))
# firebase_admin.initialize_app(cred)

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")



app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL % quote(DB_PASSWORD)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

cloudinary.config(
    cloud_name="duk7gxwvc",
    api_key="653944787632934",
    api_secret="GY20iNSIGW6CdrY1s1cDGwMKrqY",
    secure=True
)

app.config['SQLALCHEMY_ECHO'] = True
app.config['PAGE_SIZE'] = 12
app.config['ORDER'] = 'desc'

app.config["ORDER_PAGE_SIZE"] = 12
app.config["IMPORT_PAGE_SIZE"] = 20
app.config["STATISTIC_FRE_PAGE_SIZE"] = 6
app.config["STATISTIC_REVEN_PAGE_SIZE"] = 5
app.config["BOOK_PAGE_SIZE"] = 7

db = SQLAlchemy(app=app)
login = LoginManager(app)

# Register the custom filter in Jinja2
app.jinja_env.filters['currency'] = format_currency_filter
app.jinja_env.filters['datetime'] = format_datetime_filter
app.jinja_env.filters['date'] = format_date_VN()
