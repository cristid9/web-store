## @package product
#
#
#
#

from main import db

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
