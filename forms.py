from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, FloatField,
    SelectField, IntegerField, FileField
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

# Dropdown choices
GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]

WORK_TYPE_CHOICES = [
    ("children", "Children"),
    ("Govt_job", "Govt Job"),
    ("Never_worked", "Never Worked"),
    ("Private", "Private"),
    ("Self-employed", "Self-employed"),
]

RESIDENCE_CHOICES = [("Rural", "Rural"), ("Urban", "Urban")]

SMOKING_CHOICES = [
    ("formerly smoked", "Formerly smoked"),
    ("never smoked", "Never smoked"),
    ("smokes", "Smokes"),
    ("Unknown", "Unknown"),
]

YES_NO_CHOICES = [(0, "No"), (1, "Yes")]  # store as ints


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=72)])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=72)])
    submit = SubmitField("Login")


class PatientForm(FlaskForm):
    external_id = IntegerField("Patient ID", validators=[DataRequired()])
    gender = SelectField("Gender", choices=GENDER_CHOICES, validators=[DataRequired()])

    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=0, max=120)])

    # coerce=int makes values 0/1 instead of "0"/"1"
    hypertension = SelectField(
        "Hypertension",
        choices=YES_NO_CHOICES,
        coerce=int,
        validators=[DataRequired()]
    )

    ever_married = SelectField(
        "Ever Married",
        choices=[("Yes", "Yes"), ("No", "No")],
        validators=[DataRequired()]
    )

    work_type = SelectField("Work Type", choices=WORK_TYPE_CHOICES, validators=[DataRequired()])
    residence_type = SelectField("Residence Type", choices=RESIDENCE_CHOICES, validators=[DataRequired()])

    avg_glucose_level = FloatField("Avg Glucose Level", validators=[DataRequired()])
    bmi = FloatField("BMI", validators=[Optional()])

    smoking_status = SelectField("Smoking Status", choices=SMOKING_CHOICES, validators=[DataRequired()])

    stroke = SelectField(
        "Stroke",
        choices=YES_NO_CHOICES,
        coerce=int,
        validators=[DataRequired()]
    )

    submit = SubmitField("Save")


class CSVUploadForm(FlaskForm):
    file = FileField("Upload CSV File", validators=[DataRequired()])
    submit = SubmitField("Upload")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired()]
    )
    submit = SubmitField("Change Password")
