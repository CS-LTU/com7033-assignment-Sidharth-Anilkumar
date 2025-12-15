import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # Use strong random key if not set in environment
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)

    # Database stored inside instance folder
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'stroke_app.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF Protection
    WTF_CSRF_ENABLED = True

    # Secure session cookies
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Set this to True only if you deploy with HTTPS
    SESSION_COOKIE_SECURE = False

