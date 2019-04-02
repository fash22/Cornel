from flask import Blueprint, render_template, request, make_response, url_for, abort, jsonify, redirect
import flask_login as session_login
from authentication.forms import LoginInformationForm
from models import User
from werkzeug.exceptions import BadRequest
blueprint = Blueprint('authentication', __name__, url_prefix='/authentication', static_folder='static', template_folder='templates')

login_manager = session_login.LoginManager()

def user_to_dict(user_obj):
    """ Returns the `authentication.models.User` dictionary representation """
    u = {
        'id': user_obj.id,
        'username': user_obj.username,
        'password_hash': user_obj.password_hash,
        'email': user_obj.email,
        'firstname': user_obj.firstname,
        'middlename': user_obj.middlename,
        'lastname': user_obj.lastname,
        'gender': user_obj.gender,
        'account_type': user_obj.account_type
    }

    return u

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first_or_404()

@blueprint.route('/', methods=['GET', 'POST'])
def login():
    form = LoginInformationForm()
    if request.method == 'POST':
        visitor = User.query.filter_by(username=request.form['username']).first_or_404()
        if visitor.verify_password(request.form['password']):
            session_login.login_user(visitor)
            return make_response(jsonify(user_to_dict(visitor)))
        else:
            return abort(BadRequest.code) # Bad Request
    return render_template('login.html', form=form)

@blueprint.route('/logout')
@session_login.login_required
def logout():
    session_login.logout_user()
    return redirect(url_for('authentication.login'))