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
	price = db.Column(db.Float, nullable=False)
	stock = db.Column(db.Integer, nullable=False)


	def __init__(self, name, price, stock):
		self.name = name
		self.price = price
		self.stock = stock

	def __repr__(self):
		return "<Product(%r, %r, %)>" % (self.name, self.price, self.stock)


class ProductComments(db.Column):
	__tablename__ = 'productcomments_table'

	id = db.Column(db.Integer, primary_key=True)
	data = db.Column(db.DateTime, nullable=False)
	comment = db.Column(db.String, nullable=False)
	productId = db.Column(db.Integer, db.ForeignKey('product_table.id'))
	userId = db.Column(db.Integer, db.ForeignKey('productcomments_table.id'))

	def __init__(self, user, product, comment):
		self.user = user
		self.product = product
		self.comment = comment

	def __repr__(self):
		return "<ProductComment(%r, %r, %r)>" % (self.user, self.product, 
					self.comment)


		






