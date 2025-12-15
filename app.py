from flask import (
    Flask, render_template, redirect,
    url_for, flash, request, send_file
)
from flask_login import (
    LoginManager, login_user,
    logout_user, login_required,
    current_user
)
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from models import db, User, Patient
from forms import (
    RegistrationForm, LoginForm,
    PatientForm, CSVUploadForm,
    ChangePasswordForm
)
from config import Config

import os
import pandas as pd


# APP FACTORY
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print("DATABASE PATH:", app.config["SQLALCHEMY_DATABASE_URI"])

    # Security
    CSRFProtect(app)

    # Ensure instance directory exists
    os.makedirs("instance", exist_ok=True)

    # Database
    db.init_app(app)

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    
    # HELPER: BUILD FILTERED PATIENT QUERY
    def build_patient_query():
        search = request.args.get("search", "").strip()
        gender = request.args.get("gender", "")
        stroke = request.args.get("stroke", "")
        age_min = request.args.get("age_min", "")
        age_max = request.args.get("age_max", "")

        query = Patient.query

        if search:
            query = query.filter(
                (Patient.gender.ilike(f"%{search}%")) |
                (Patient.smoking_status.ilike(f"%{search}%"))
            )

            if search.isdigit():
                query = query.union(
                    Patient.query.filter_by(
                        external_id=int(search)
                    )
                )

        if gender:
            query = query.filter_by(gender=gender)

        if stroke != "":
            query = query.filter_by(stroke=bool(int(stroke)))

        if age_min.isdigit():
            query = query.filter(Patient.age >= int(age_min))

        if age_max.isdigit():
            query = query.filter(Patient.age <= int(age_max))

        return query

    
    # PUBLIC HOME
    @app.route("/")
    def home():
        return render_template("home.html")

    
    # DASHBOARD
    @app.route("/dashboard")
    @login_required
    def dashboard():
        total_patients = Patient.query.count()
        return render_template(
            "index.html",
            total_patients=total_patients
        )

    
    # AUTH
    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(
                email=form.email.data
            ).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
            flash("Invalid credentials.", "danger")
        return render_template("login.html", form=form)

    @app.route("/change-password", methods=["GET", "POST"])
    @login_required
    def change_password():
        form = ChangePasswordForm()

        if form.validate_on_submit():
            if not current_user.check_password(form.current_password.data):
                flash("Current password is incorrect.", "danger")
                return redirect(url_for("change_password"))

            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Password updated successfully.", "success")
            return redirect(url_for("dashboard"))

        return render_template("change_password.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("home"))

    
    # PATIENT LIST (FILTERED VIEW)
    @app.route("/patients")
    @login_required
    def patients():
        query = build_patient_query()
        return render_template(
            "patients.html",
            patients=query.all()
        )

    
    # ADD PATIENT
    @app.route("/patients/new", methods=["GET", "POST"])
    @login_required
    def new_patient():
        form = PatientForm()
        if form.validate_on_submit():
            patient = Patient(
                external_id=form.external_id.data,
                gender=form.gender.data,
                age=form.age.data,
                hypertension=bool(int(form.hypertension.data)),
                ever_married=form.ever_married.data,
                work_type=form.work_type.data,
                residence_type=form.residence_type.data,
                avg_glucose_level=form.avg_glucose_level.data,
                bmi=form.bmi.data,
                smoking_status=form.smoking_status.data,
                stroke=bool(int(form.stroke.data)),
            )
            db.session.add(patient)
            db.session.commit()
            flash("Patient added.", "success")
            return redirect(url_for("patients"))
        return render_template("patient_form.html", form=form)

    
    # EDIT PATIENT
    @app.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_patient(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        form = PatientForm(obj=patient)

        if form.validate_on_submit():
            patient.external_id = form.external_id.data
            patient.gender = form.gender.data
            patient.age = form.age.data
            patient.hypertension = bool(int(form.hypertension.data))
            patient.ever_married = form.ever_married.data
            patient.work_type = form.work_type.data
            patient.residence_type = form.residence_type.data
            patient.avg_glucose_level = form.avg_glucose_level.data
            patient.bmi = form.bmi.data
            patient.smoking_status = form.smoking_status.data
            patient.stroke = bool(int(form.stroke.data))

            db.session.commit()
            flash("Patient updated.", "success")
            return redirect(url_for("patients"))

        return render_template("edit_patient.html", form=form)


    # DELETE PATIENT
    @app.route("/patients/<int:patient_id>/delete", methods=["POST"])
    @login_required
    def delete_patient(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        flash("Patient deleted.", "warning")
        return redirect(url_for("patients"))

    
    # CSV UPLOAD
    @app.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload():
        form = CSVUploadForm()

        if form.validate_on_submit():
            file = form.file.data
            filename = secure_filename(file.filename)
            filepath = os.path.join("instance", filename)
            file.save(filepath)

            df = pd.read_csv(filepath)
            df.columns = df.columns.str.strip().str.lower()

            imported = skipped = 0

            for _, row in df.iterrows():
                if Patient.query.filter_by(
                    external_id=row.get("id")
                ).first():
                    skipped += 1
                    continue

                patient = Patient(
                    external_id=row.get("id"),
                    gender=row.get("gender"),
                    age=row.get("age"),
                    hypertension=bool(int(row.get("hypertension", 0))),
                    ever_married=row.get("ever_married"),
                    work_type=row.get("work_type"),
                    residence_type=row.get("residence_type"),
                    avg_glucose_level=row.get("avg_glucose_level"),
                    bmi=row.get("bmi"),
                    smoking_status=row.get("smoking_status"),
                    stroke=bool(int(row.get("stroke", 0))),
                )

                db.session.add(patient)
                imported += 1

            db.session.commit()
            flash(
                f"Upload complete. Imported {imported}, skipped {skipped}.",
                "success"
            )
            return redirect(url_for("patients"))

        return render_template("upload.html", form=form)

    
    # EXPORT FILTERED CSV
    @app.route("/export_csv")
    @login_required
    def export_csv():
        query = build_patient_query()
        patients = query.all()

        filepath = os.path.join(
            "instance", "exported_patients.csv"
        )

        df = pd.DataFrame([{
            "id": p.external_id,
            "gender": p.gender,
            "age": p.age,
            "hypertension": int(p.hypertension),
            "ever_married": p.ever_married,
            "work_type": p.work_type,
            "residence_type": p.residence_type,
            "avg_glucose_level": p.avg_glucose_level,
            "bmi": p.bmi,
            "smoking_status": p.smoking_status,
            "stroke": int(p.stroke),
        } for p in patients])

        df.to_csv(filepath, index=False)
        return send_file(filepath, as_attachment=True)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=False)
