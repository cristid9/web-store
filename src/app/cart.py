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
	
	def addToCart(self, productId):
		self.items[productId] = 0
		
	def deleteFromCart(self, productId):
		del self.items[productId]
	
	def updateQuantity(self, newQuantity):
		pass
	
	def getTotal(self):
		pass
	
	
