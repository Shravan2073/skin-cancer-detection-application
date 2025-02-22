from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User, Patient
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = 'patient'  # Only patients can register themselves

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        patient = Patient(user=user, date_of_birth=datetime.strptime(request.form['dob'], '%Y-%m-%d'))
        db.session.add(patient)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

