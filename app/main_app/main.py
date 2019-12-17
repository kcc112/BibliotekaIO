from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main_app


@main_app.route('/')
def route():
    return redirect(url_for('registration_login_app.login'))


@main_app.route('/home')
@login_required
def home():
    return render_template('/main/application_base.html')
