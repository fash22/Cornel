from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, EqualTo

class LoginInformationForm(FlaskForm):
    """ Form for accessing user login information"""
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    

class UserInformationForm(FlaskForm):
    """ Form for adding and editing user account information """
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    vpassword = PasswordField('Verify Password', validators=[Required(), EqualTo(password)])
    email = EmailField('E-mail Address', validators=[Required()])
    firstname = StringField('First Name', validators=[Required()])
    middlename = StringField('Middle Name', validators=[Required()])
    lastname = StringField('Last Name', validators=[Required()])
    gender = SelectField('Gender', validators=[Required()], choices=[('0', 'Female'),('1', 'Male')])
    account_type = SelectField('Account Type', choices=[('0','Developer'),('1','Supplies Officer'),('2','Cashier'),('3','Customer')])