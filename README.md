STROKE MANAGEMENT SYSTEM


Overview

The Stroke Management System is a secure web application developed using Flask and SQLite.
It allows authorised users to manage patient data related to stroke risk in a safe, organised, and user-friendly way. The system supports secure login, patient record management, dataset upload and export, and follows good secure programming practices.

Main Features

•	Secure user registration and login
•	Password hashing using bcrypt
•	CSRF protection on all forms
•	Add, edit, view, and delete individual patient records
•	Upload patient data using CSV files
•	Replace or delete entire datasets
•	Filter patient records by gender, stroke status, and search terms
•	Export patient data to CSV
•	Change password functionality
•	Clean and accessible user interface designed using Bootstrap

Technologies Used

•	Python (Flask)
•	SQLite database
•	Flask-Login for authentication
•	Flask-WTF for form handling and CSRF protection
•	Pandas for CSV import and export
•	Bootstrap 5 for the user interface


Installation Instructions	

1. Clone the Repository

git clone https://github.com/CS-LTU/com7033-assignment-Sidharth-Anilkumar.git

cd com7033-assignment-Sidharth-Anilkumar


2. Create and Activate a Virtual Environment

python -m venv venv

Activate it:

venv\Scripts\activate


3. Install Required Packages
pip install -r requirements.txt

4. Run the Application
python app.py


The application will run at:
http://127.0.0.1:5000

Using the System

•	Register a new user account
•	Log in using your email and password
•	Upload a CSV dataset or add patients manually
•	View, filter, edit, or delete patient records
•	Export filtered patient data as a CSV file
•	Change your password if required
•	Log out when finished

Security Considerations

•	Passwords are securely hashed and never stored in plain text
•	CSRF tokens are used to protect all forms
•	Input validation is applied to forms and file uploads
•	User authentication is required to access sensitive data
•	Sessions are securely managed using Flask-Login

Ethical and Professional Practice

•	This system was developed with attention to:
•	User privacy and data protection
•	Secure handling of sensitive medical information
•	Clear and maintainable code structure
•	Responsible use of third-party libraries
•	Generative AI Declaration


Generative AI Declaration:
This assignment used generative AI for brainstorming, planning, and feedback.
