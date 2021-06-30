from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        if not user  or  not check_password_hash(user.password, password):
            flash('check your credentials.')
            return redirect(url_for('main.index'))

        login_user(user, remember=remember)

        return redirect(url_for('main.profile'))
    else:
        return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.')
            return redirect(url_for('auth.login'))

        password_hash = generate_password_hash(password, method='sha256')

        new_user = User(email=email, password=password_hash, name=name)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')

@auth.route('/logout')
def logout():
    flash('You are now logged out')
    logout_user()
    return redirect(url_for('main.index'))
