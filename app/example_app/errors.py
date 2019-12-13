from flask import render_template
from . import example_app 

@example_app.app_errorhandler(404)
def page_not_found(e):
    return render_template('/example_app/404.html'), 404
    
@example_app.app_errorhandler(500)
def internal_server_error(e):
    return render_template('/example_app/500.html'), 500