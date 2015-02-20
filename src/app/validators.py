## @package validators
#
# This file will contain all the custom validators used for the forms in this
#  app.

from wtforms.validators import ValidationError
from main import db
from user import User
from email.utils import parseaddr

## Function used as validator to check if the username is
#  unique.
#
#  @param form The current form.
#  @param field The field this validator is applied to.
#
#  @return void It doesn't return anything.
def uniqueUser(form, field):
	if User.query.filter_by(username=field.data).first():
		raise ValidationError('Username is already taken')


## Function used a validator to check if an email address is
#  valid.
#
#  @param form The current form.
#  @param field The field this validator is applied to.
#
#  @return void It doesn't return anything.
def validEmail(form, field):
	if parseaddr(field.data)[1] is None:
		raise ValidationError('Email address is not correct')

