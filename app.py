from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.secret_key = 'secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(10))

@app.route('/')
def home():
    return render_template('student/home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if user with the same email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error_message = 'User with this email already exists! Please try a different email.'
            return render_template('student/registration.html', error_message=error_message, name=name, email=email)

        # Create a new user object
        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Set registration_success variable to display success message
        registration_success = True

        return render_template('student/registration.html', registration_success=registration_success)

    return render_template('student/registration.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return redirect(url_for('login'))

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user or user.password != password:
            flash('Invalid email or password!', 'error')
            return redirect(url_for('login'))

        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('student/login.html')

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student_profile'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher_profile'))
    flash('Please log in to access the profile page.', 'error')
    return redirect(url_for('login'))




@app.route('/profile/student')
def student_profile():
    if current_user.is_authenticated and current_user.role == 'student':
        return render_template('student/student_profile.html', current_user=current_user)
    return redirect(url_for('login'))

@app.route('/profile/teacher')
def teacher_profile():
    if current_user.is_authenticated and current_user.role == 'teacher':
        return render_template('student/teacher_profile.html', current_user=current_user)
    else:
        flash('Invalid email or password for teacher role.', 'error')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
