from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, logout_user
from application.bp.authentication.forms import RegisterForm, LoginForm
from application.database import User, db
from werkzeug.security import check_password_hash

authentication = Blueprint('authentication', __name__, template_folder='templates')

@authentication.route('/registration', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('authentication.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('registration.html', form=form)
        
        # Create new user
        user = User.create(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('authentication.login'))
    
    return render_template('registration.html', form=form)


@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('authentication.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('User Not Found', 'error')
            return render_template('login.html', form=form)
        
        if not check_password_hash(user.password, form.password.data):
            flash('Password Incorrect', 'error')
            return render_template('login.html', form=form)
        
        login_user(user)
        return redirect(url_for('authentication.dashboard'))
    
    return render_template('login.html', form=form)


@authentication.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage.homepage'))
