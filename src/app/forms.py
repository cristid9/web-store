## @package forms
#  
#  This file will contain all the logical representation of all the forms used
#  in the aplication. 

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo

class SingupForm(Form):
	name = TextField('name', [Required()])
	username = TextField('username', [Required()])
	email = TextField('email', [Required()])
	password = PasswordField('password', [
		Required(),
		EqualTo('confirm', message="Parolele nu se potrivesc")
	])
	confirm = PasswordField('repeat_password')
