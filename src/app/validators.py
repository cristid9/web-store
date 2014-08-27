## @package validators
#
#  This file will contain all the custom validators used for the forms in this
#  app.

from wtforms.validators import ValidationError
from main import db
from user import User
from email.utils import parseaddr

def uniqueUser(form, field):
	if User.query.filter_by(username=field.data).first():
		raise ValidationError('Username is already taken')

def validEmail(form, field):
	if parseaddr(field.data)[1] is None:
		raise ValidationError('Email address is not correct')

def validPassword(form, field):
	pass # implement it later
