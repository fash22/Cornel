"""
The database model definition of the whole web application
"""

from server import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """
    Database Model for User Accounts
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    firstname = db.Column(db.String(120)) 
    middlename = db.Column(db.String(120)) 
    lastname = db.Column(db.String(120))
    gender = db.Column(db.Boolean)
    account_type = db.Column(db.Integer())

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)