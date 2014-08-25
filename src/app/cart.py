## @package chart
#
#
#

from main import db

##
#
#
#
class Cart(object):
	items = {}
	
	def __init__(self):
		pass
	
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

class Order(db.Model):
	id = db.Column(db.Integer)
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












	
