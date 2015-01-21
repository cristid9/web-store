## @package forms
#  
#  This file will contain all the logical representation of all the forms used
#  in the aplication. 

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import Required, Email, EqualTo, length
from validators import uniqueUser, validEmail

class SingupForm(Form):
	name = TextField('name', [Required()])
	username = TextField('username', [Required(), uniqueUser])
	email = TextField('email', [validEmail])
	password = PasswordField('password', [
		Required(),
		EqualTo('confirm', message="Parolele nu se potrivesc")
	])
	confirm = PasswordField('repeat_password')


class LoginForm(Form):
	username = TextField('username', [Required()])
	password = PasswordField('password', [Required()])


class AddressForm(Form):
	phone = TextField('phone', [Required()])
	email = TextField('email', [Required()])
	region = TextField('region', [Required()])
	city = TextField('city', [Required()])
	address = TextField('address', [Required()])


class ContactForm(Form):
	name = TextField('name', [Required()])
	email = TextField('email', [Required()])
	message = TextAreaField('message', [Required(), length(max=500)])

class AddNewProductForm(Form):
	name = TextField('name', [Required()])
	price = TextField('price', [Required()])
	stock = TextField('stock', [Required()])
	description = TextAreaField('description', [Required()])
	category = TextField('category', [Required()])