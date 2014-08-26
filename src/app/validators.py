## @package validators
#
#  This file will contain all the custom validators used for the forms in this
#  app.

from wtforms.validators import ValidationError
from main import db
from user import User

def uniqueUser(form, field):
	if User.query.filter_by(username=field.data):
		raise ValidationError('Username is already taken')
