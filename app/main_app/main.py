from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main_app


@main_app.route('/')
def route():
    return redirect(url_for('registration_login_app.login'))
