## @package chart
#
#
#

from main import db
from flask import session

##
#
#
#
class Cart(object):
	items = {}
	
	def __init__(self):
		if "cart" in session.keys():
			self.items = session["cart"]
		else:
			session["cart"] = {}
	
	def addToCart(self, productId, price):
		self.items[productId] = {
			"price": price,
			"quantity": 0
		}
	
	def deleteFromCart(self, productId):
		del self.items[productId]
	
	def updateQuantity(self, productId, toAdd):
		self.items[productId]["quantity"] += toAdd

	def getTotal(self):
		total = 0
		for item in items:
			total += item["qunatity"] * item["price"]
		total += (24.0/100) * total
		return total	

	def __del__(self):
		session["cart"] = self.items

class Order(db.Model):
	__tablename__ = "order_table"

	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	total = db.Column(db.Float)
	userId = db.Column(db.Integer, db.ForeignKey('user_table.id'))
	buyedProductId = db.Column(db.Integer, db.ForeignKey('product_table.id'))

	def __init__(self, total, userId, buyedProductId):
		self.total = total
		self.userId = userId
		self.buyedProductId = buyedProductId

	def __repr__(self):
		return "<Order(%r)>" % self.total












	
