from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from urllib.parse import quote
from dotenv import dotenv_values, load_dotenv
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)
load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")
# SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


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

