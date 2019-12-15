from flask import render_template
from . import owner


@owner.app_errorhandler(404)
def page_not_found(e):
    return render_template('owner/404.html'), 404


@owner.app_errorhandler(500)
def internal_server_error(e):
    return render_template('owner/500.html'), 500
