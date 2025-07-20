from sqlalchemy import Column, Integer, String, Boolean, Text, Date, DateTime, Enum
from app import db, app
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import datetime
import hashlib

class UserRole(RoleEnum):
    LIBRARIAN = 1
    USER = 2

class UserType(RoleEnum):
    DEFAULT = 1
    GOOGLE = 2

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=False)
    sex = Column(Boolean, nullable=False, default=True)
    email = Column(String(50), nullable=True, unique=True)
    phone_number = Column(String(10), nullable=True, unique=True)
    date_of_birth = Column(Date, nullable=True)
    avt_url = Column(Text,
                     default="https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg")
    isActive = Column(Boolean, default=True)
    last_access = Column(DateTime, default=datetime.utcnow)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    user_type = Column(Enum(UserType), default=UserType.DEFAULT)

    def to_local_storge(self):
        return {
            "user_id": self.user_id,
        }

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return self.isActive

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)
