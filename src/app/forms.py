## @package forms
#  
#  This file will contain all the logical representation of all the forms used
#  in the aplication. 

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo
from validators import uniqueUser

class SingupForm(Form):
	name = TextField('name', [Required()])
	username = TextField('username', [Required(), uniqueUser])
	password = PasswordField('password', [
		Required(),
		EqualTo('confirm', message="Parolele nu se potrivesc")
	])
	confirm = PasswordField('repeat_password')
