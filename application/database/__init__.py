"""
Database Initialization and Models
"""
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, email, password, active=True):
        self.email = email
        self.password = User.set_password(password)
        self.active = active

    @classmethod
    def create(cls, email, password):
        return cls(email, password)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def find_user_by_id(cls, user_id):
        return cls.query.filter(cls.id == user_id).first()

    @classmethod
    def record_count(cls):
        return cls.query.count()

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active