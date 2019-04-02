from flask import Blueprint, render_template, request, make_response, url_for, abort, jsonify, redirect
import flask_login as session_login
from authentication.forms import LoginInformationForm, UserInformationForm
from models import User, db
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
from sqlalchemy.exc import IntegrityError

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

# ==============================ACCOUNT AUTHORIZATION DECORATORs==============================
from functools import wraps
def developer_required(func):
    """ Decorator to restrict access from other accounts except for developers """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session_login.current_user.account_type != 0:               # 0 - Developer Account
            return abort(Unauthorized.code)
        else:
            return func(*args, **kwargs)

    return wrapper

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



# DEVELOPER ROUTES for User Account Management
@blueprint.route('/users')
@session_login.login_required
@developer_required
def users():
    """ Lists all users """                 
    form = UserInformationForm()
    users = User.query.all()
    if request.args.get('q', '') == 'users':                    # API request
        users_dict = list()
        for user in users:
            users_dict.append(user_to_dict(user))
        return make_response(jsonify(users_dict))
    return render_template('users/users.html', users=users)

@blueprint.route('/user/create', methods=['GET', 'POST'])
@session_login.login_required
@developer_required
def create_user():
    form = UserInformationForm()
    if request.method == 'POST':
        u = User(
            username=form.username.data, email=form.email.data, password=form.password.data,
            firstname=form.firstname.data, middlename=form.middlename.data,lastname=form.lastname.data,
            account_type=int(form.account_type.data), gender=int(form.gender.data)
        )
        try:
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('authentication.users'))
        except IntegrityError as err:
            db.session.rollback()
            return render_template('users/user.html', form=form, type='Add', error='Username was already used')
    return render_template('users/create.html', form=form, type='Add')

@blueprint.route('/user/update/<username>', methods=['GET', 'POST'])
@session_login.login_required
@developer_required
def update_user(username):
    u = User.query.filter_by(username=username).first_or_404()
    form = UserInformationForm()
    if request.method == 'POST':
        u.username=form.username.data
        u.email=form.email.data
        u.password=form.password.data
        u.firstname=form.firstname.data
        u.middlename=form.middlename.data
        u.lastname=form.lastname.data
        u.account_type=int(form.account_type.data)
        u.gender=int(form.gender.data)

        try:
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('authentication.users'))
        except IntegrityError as err:
            db.session.rollback()
            return render_template('users/update.html', form=form, error='Username was already used')

    return render_template('users/update.html', form=form, user=u)

@blueprint.route('/user/delete/<username>')
@session_login.login_required
@developer_required
def delete_user(username):
    u = User.query.filter_by(username=username).first_or_404()
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for('authentication.users'))