## @package chart
#
#
#

from main import db
from flask import session
from product import Product
from datetime import datetime

##
#
#
#
class Cart(object):
        
            
	def __init__(self, cart, shipping):
		self.items = cart
		self.shipping =float(shipping)

	def addToCart(self, productId, price):
            self.items[productId] = {
                "price": price,
                "quantity": 1
            }
            
	def deleteFromCart(self, productId):
		del self.items[productId]
	
	def updateQuantity(self, productId, newQuantity):
		self.items[productId]["quantity"] = newQuantity

	def getTotal(self):
	    total = 0
	    for item in self.items:
		total += self.items[item]["quantity"] * \
                    self.items[item]["price"]
	    return total + float(self.shipping)	
	
	## Because I can't perform queries from templates I need a list with all 
	#  products buyed by the user.
	def getProductData(self):
	    data = []
	    for id in self.items:
		data.append(Product.query.get(id))

	    return data

	def updateShipping(self, price):
		self.shipping = price

class Order(db.Model):
	__tablename__ = "order_table"

	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	total = db.Column(db.Float)
	userId = db.Column(db.Integer, db.ForeignKey('user_table.id'))
	buyedProductId = db.Column(db.Integer, db.ForeignKey('product_table.id'))
	address = db.Column(db.Integer, db.ForeignKey('userdata_table.id'))

	def __init__(self, total, userId, buyedProductId):
		self.total = total
		self.userId = userId
		self.buyedProductId = buyedProductId
		date = datetime.utcnow()
	def __repr__(self):
		return "<Order(%r)>" % self.total

class ShippingMethods(db.Model):
	__tablename__ = 'shipping_methods_table'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	price = db.Column(db.String, nullable=False)
	deliveryTime = db.Column(db.Float, nullable=False)
	area = db.Column(db.String, nullable=False)
	address = db.Column(db.Integer, db.ForeignKey('userdata_table.id'))

	def __init__(self, name, price, deliveryTime, area):
		self.name = name
		self.price = price
		self.deliveryTime = deliveryTime
		self.area = area

	def __repr__():
		return "ShippingMethods(%r)" % self.name 










	
