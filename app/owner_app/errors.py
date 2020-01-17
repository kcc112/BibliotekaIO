from flask import render_template
from . import owner_app


@owner_app.app_errorhandler(404)
def page_not_found(e):
    return render_template('owner/404.html'), 404


@owner_app.app_errorhandler(500)
def internal_server_error(e):
    return render_template('owner/500.html'), 500
