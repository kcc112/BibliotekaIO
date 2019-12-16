from flask import render_template, flash, redirect, url_for, request
from . import registration_login_app
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from ..models import User
from werkzeug.urls import url_parse
from .. import db


@registration_login_app.route('/index')
def index():
    return redirect(url_for('main_app.home'))


@registration_login_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('registration_login_app.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('registration_login_app.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page) != '':
            next_page = url_for('registration_login_app.login')
            if user.user_type == 'client':
                next_page = url_for('registration_login_app.index')
            if user.user_type == 'employee':
                next_page = url_for('owner_app.ownerView')
        return redirect(next_page)
    return render_template('/registration_login/login.html', title='Sign In', form=form)


@registration_login_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('registration_login_app.login'))


@registration_login_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('registration_login_app.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, user_type='client')
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('registration_login_app.login'))
    return render_template('/registration_login/register.html', title='Register', form=form)
