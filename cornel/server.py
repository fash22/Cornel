from flask import Flask, render_template, url_for, redirect, abort
from config import Configuration, DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Extension Modules
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Hello, world!'


# <<<<<<<<<<<<<<< Global Error Handlers
from werkzeug import exceptions
@app.errorhandler(exceptions.BadRequest)
def bad_request(e):
    error = {
        'code': exceptions.BadRequest.code,
        'name': 'Bad Request',
        'desc': exceptions.BadRequest.description,
        'details': 'The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications.'
    }
    return render_template('errors/http-error.html', error=error),exceptions.BadRequest.code
@app.errorhandler(exceptions.Unauthorized)
def unauthorized(e):
    error = {
        'code': exceptions.Unauthorized.code,
        'name': 'Unauthorized',
        'desc': exceptions.Unauthorized.description,
        'details': 'The request requires user authentication. The response MUST include a WWW-Authenticate header field (section 14.47) containing a challenge blueprintlicable to the requested resource. '
    }
    return render_template('errors/http-error.html', error=error),exceptions.Unauthorized.code
@app.errorhandler(exceptions.Forbidden)
def forbidden(e):
    error = {
        'code': exceptions.Forbidden.code,
        'name': 'Forbidden',
        'desc': exceptions.Forbidden.description,
        'details': 'The server understood the request, but is refusing to fulfill it. Authorization will not help and the request SHOULD NOT be repeated.'
    }
    return render_template('errors/http-error.html', error=error),exceptions.Forbidden.code
@app.errorhandler(exceptions.NotFound)
def not_found(e):
    error = {
        'code': exceptions.NotFound.code,
        'name': 'Not Found',
        'desc': exceptions.NotFound.description,
        'details': 'The server has not found anything matching the Request-URI. No indication is given of whether the condition is temporary or permanent.'
    }
    return render_template('errors/http-error.html', error=error),exceptions.NotFound.code

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))