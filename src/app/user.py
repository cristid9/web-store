## @package user
#
#
#
#

from main import db

##
#
#
#
class User(db.Model):
	__tablename__ = 'user_table'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Integer, nullable=False)
	name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	userData = db.relationship('UserData', backref='user', lazy='dynamic')

	##
	#
	#
	#
	def __init__(self, username, name, password):
		self.username = username
		self.name = name
		self.password = password
		
	def __repr__(self):
		return "<User(%r, %r, %r)>" % (self.username, self.name, self.password)


class UserData(db.Model):
	__tablename__ = 'userdata_table'

	id = db.Column(db.Integer, primary_key=True)
	phone = db.Column(db.Integer)
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









