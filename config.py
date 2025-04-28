"""Configuration Class for Flask"""
import os
import secrets


class Config:
    """Default Config Settings"""
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', "TRUE")
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///app.db")
    SECRET_KEY = secrets.token_urlsafe(16)
    WTF_CSRF_ENABLED = True


class TestConfig(Config):
    """Test Config Settings"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"