## @package user
#
#  This module contains all the classes related to a user, independet of it's
#  state

from main import db

## Since there are 2 types of user: pending users and normal users, and both
#  have the same attributes there must be a base user class and the other
#  should extend this class.
class BaseUser(db.Model):
	__tablename__ = 'user_table'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)

	## Constructor method of the BaseUser class.
	def __init__(self, username, name, password, email):
		self.username = username
		self.name = name
		self.password = password
		# An user should have a primary email address.
		self.email = email
		
	def __repr__(self):
		return "<User(%r, %r, %r)>" % (self.username, self.name, self.password)

		
## Represents a normal user.
class User(BaseUser):
	userData = db.relationship('UserData', backref='user', lazy='dynamic')
	
	def __init__():
		pass



class UserData(db.Model):
	__tablename__ = 'userdata_table'

	id = db.Column(db.Integer, primary_key=True)
	phone = db.Column(db.String)
	email = db.Column(db.String)
	region = db.Column(db.String)
	city = db.Column(db.String)
	address = db.Column(db.String)
	userId = db.Column(db.Integer, db.ForeignKey('user_table.id'))

	def __init__(self, phone=None, email=None, region=None, city=None,
				 address=None):
		self.phone = phone
		self.email = email
		self.region = region
		self.city = city
		self.address = address

	def __repr__(self):
		return "<UserData(%r, %r, %r, %r, %r)>" % (self.phone, self.email,
				self.region, self.city, self.address)









