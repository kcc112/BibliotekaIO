from flask import render_template, session, redirect, url_for, current_app, request
from app import db
from app.models import User
from app.models import WorkSchedule
from app.owner import owner
from datetime import date


@owner.route('/')
def index():
    return render_template('owner/index.html')