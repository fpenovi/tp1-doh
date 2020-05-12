from werkzeug.exceptions import BadRequest, NotFound

def handle_error(e):
    return {'error': e.description}, e.code

def set_error_handlers(app):
    for ex in [BadRequest, NotFound]:
        app.add_error_handler(ex, handle_error)

