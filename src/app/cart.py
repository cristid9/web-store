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
		for item in items.keys():
			db.session.query()
	
	
