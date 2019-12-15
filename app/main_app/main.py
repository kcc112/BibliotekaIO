from flask import render_template
from . import main_app


@main_app.route('/')
def base():
    return render_template('/main/application_base.html')
