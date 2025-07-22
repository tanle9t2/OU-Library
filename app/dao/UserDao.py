import pdb

import app.model.User
from app.exception.BadRequestError import BadRequestError
from app.exception.NotFoundError import NotFoundError
from app.model.User import User
from sqlalchemy import and_
import hashlib
from app import db
import cloudinary.uploader
from app.model.User import UserRole, UserType
import json
from app.model.User import User
from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload
import validators



def auth_user(identifier, password=None, role=None, user_type=None):
    if not identifier:
        return None

    query = User.query.filter(
        or_(
            User.username == identifier.strip(),
            User.email == identifier.strip()
        )
    )

    # Nếu login bằng username/password thông thường
    if user_type != UserType.GOOGLE:
        if not password:
            return None
        password_hash = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
        query = query.filter(User.password == password_hash)

    # Nếu có kiểm tra vai trò
    if role:
        query = query.filter(User.user_role == role)

    if user_type:
        query = query.filter(User.user_type == user_type)

    return query.first()


def add_user(first_name, last_name, username, password, email, phone_number, avt_url=None, sex=None,
             date_of_birth=None, isActive=None, last_access=None,  role=UserRole.USER, user_type=None):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    # Tạo bản ghi User
    u = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        email=email,
        avt_url=avt_url or 'https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg',
        sex=sex,
        phone_number=phone_number,
        date_of_birth=date_of_birth,
        isActive=isActive,
        last_access=last_access,
        user_role=role,
        user_type=user_type
    )
    db.session.add(u)
    db.session.commit()

def add_account_user(first_name, last_name, username, password, email, avt_url=None, sex=None, phone_number=None,
                 date_of_birth=None, isActive=None, last_access=None):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    user = find_by_phone_number(phone_number)

    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.password = password
    user.email=email
    user.avt_url=avt_url or 'https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg'
    user.sex=True
    user.phone_number=phone_number
    user.date_of_birth=date_of_birth
    user.isActive=isActive
    user.last_access=last_access

    db.session.commit()

def add_employee(first_name, last_name, username, password, email, avt_url=None, sex=None, phone_number=None,
                 date_of_birth=None, isActive=None, last_access=None, user_role=None):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    # Tạo bản ghi User
    u = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        email=email,
        avt_url=avt_url or 'https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg',
        sex=sex,
        phone_number=phone_number,
        date_of_birth=date_of_birth,
        isActive=isActive,
        last_access=last_access,
        user_role=user_role  # Thêm user_role vào đây
    )

    db.session.add(u)
    db.session.commit()


def find_by_customer_id_phone_number(user_id, phone_number):
    user = User.query
    user = user.filter(User.user_id == user_id, User.phone_number == phone_number).first()

    if not user:
        raise BadRequestError("Không tồn tại user với số điện thoại tương ứng")

    return user

def delete_address(user_id, address_id):
    user = User.query.get(user_id)

    for a in user.address:
        if a.address_id == address_id:
            a.is_active = False
            db.session.commit()
            return a

    raise NotFoundError("Not found address")


def find_by_phone_number(phone_number):
    query = User.query
    query = query.filter(User.phone_number == phone_number)
    return query.first()


def find_customer_phone_number(phone_number):
    obj = [{
        'id': item[0],
        'fullname': item[1] + " " + item[2],
        'phone_number': item[3]
    }
        for item in db.session.execute(
            select(User.user_id, User.first_name, User.last_name, User.phone_number)
            .where(and_(User.phone_number.contains(phone_number), User.user_role == UserRole.USER)))]
    return obj


"""
    Tra ve 1: username, email, so dien thoai da ton tai => Khong  the tao
    Tra ve 0: username, email, so dien thoai chua ton tai => Co the tao
"""


def check_exists(username=None, email=None, phone_number=None):
    if username and User.query.filter_by(username=username).first():
        return 1

    if email and User.query.filter_by(email=email).first():
        return 1

    if phone_number and User.query.filter_by(phone_number=phone_number).first():
        return 1

    return 0


def check_exists_email(email=None):
    if email and User.query.filter_by(email=email).first():
        return True
    return False


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_email(email):
    return db.session.query(User).filter_by(email=email).first()


def is_valid_email(email):
    return validators.email(email)


def update_password(username, password):
    hashed_password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    user = db.session.query(User).filter_by(username=username.strip()).first()
    if user:
        user.password = hashed_password
        db.session.commit()
