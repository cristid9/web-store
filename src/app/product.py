## @package product
#
#
#
#

from main import db
from datetime import datetime

##
#
#
#
class Product(db.Model):
	__tablename__ = 'product_table'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	price = db.Column(db.Float, nullable=False)
	stock = db.Column(db.Integer, nullable=False)
	comments = db.relationship('ProductComment', backref='product', 
								lazy='dynamic')


	def __init__(self, name, price, stock):
		self.name = name
		self.price = price
		self.stock = stock

	def __repr__(self):
		return "<Product(%r, %r, %)>" % (self.name, self.price, self.stock)


class ProductComment(db.Model):
	__tablename__ = 'product_comments_table'
	id = db.Column(db.Integer, primary_key=True)
	comment = db.Column(db.String, nullable=False)
	userId = db.Column(db.Integer, db.ForeignKey('user_table.id'))
	productId = db.Column(db.Integer, db.ForeignKey('product_table.id'))

	def __init__(self, comment, userId):
		self.comment = comment	
		self.userId = userId
		
	def __repr__(self):
		return "<ProductComment(%r)>" % self.comment
		
		
		
			






