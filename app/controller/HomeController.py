from flask import Blueprint
from flask import render_template, request, redirect, url_for, session

index_bp = Blueprint('index', __name__)

@index_bp.route("/")
def index():
    return render_template("home.html")