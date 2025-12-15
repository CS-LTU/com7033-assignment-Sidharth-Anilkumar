from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import secrets

db = SQLAlchemy()



# USER MODEL
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # 🔐 Password reset support
    reset_token = db.Column(
        db.String(128),
        nullable=True
    )

    reset_token_expiry = db.Column(
        db.DateTime,
        nullable=True
    )

    
    # PASSWORD METHODS
    def set_password(self, password: str):
        """Hash and store a password securely."""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a password against stored hash."""
        return bcrypt.verify(password, self.password_hash)

    
    # RESET TOKEN METHODS
    def generate_reset_token(self) -> str:
        """Generate a secure, time-limited reset token."""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
        return self.reset_token

    def clear_reset_token(self):
        """Invalidate reset token after use."""
        self.reset_token = None
        self.reset_token_expiry = None

    def is_reset_token_valid(self, token: str) -> bool:
        """Check if reset token is valid and not expired."""
        return (
            self.reset_token == token and
            self.reset_token_expiry is not None and
            datetime.utcnow() < self.reset_token_expiry
        )



# DATASET MODEL
class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(120),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    uploaded_by_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    uploader = db.relationship(
        "User",
        backref="datasets"
    )

    # When a dataset is deleted, all patients are deleted too
    patients = db.relationship(
        "Patient",
        backref="dataset",
        cascade="all, delete-orphan"
    )



# PATIENT MODEL
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    external_id = db.Column(
        db.Integer,
        unique=True,
        nullable=False
    )

    gender = db.Column(
        db.String(10),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    hypertension = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    ever_married = db.Column(
        db.String(10),
        nullable=False
    )

    work_type = db.Column(
        db.String(20),
        nullable=False
    )

    residence_type = db.Column(
        db.String(10),
        nullable=False
    )

    avg_glucose_level = db.Column(
        db.Float,
        nullable=False
    )

    bmi = db.Column(
        db.Float,
        nullable=True
    )

    smoking_status = db.Column(
        db.String(30),
        nullable=False
    )

    stroke = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # Link patient to dataset
    dataset_id = db.Column(
        db.Integer,
        db.ForeignKey("dataset.id"),
        nullable=True
    )
