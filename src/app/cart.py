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
        self.shipping = float(shipping)

    def addToCart(self, productId, price):
        self.items[productId] = {
            "price": price,
            "quantity": 1
        }

    def is_empty(self):
        return not bool(self.items)

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
    # products buyed by the user.

    def getProductData(self):
        data = []
        for product_id in self.items:
            data.append(Product.query.get(product_id))

        return data

    def updateShipping(self, price):
        self.shipping = price

    def get_products_ids(self):
        return self.items.keys()

    def get_quantity_by_id(self, product_id):
        return self.items[product_id]["quantity"]

class Order(db.Model):
    __tablename__ = "order_table"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    total = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    address = db.Column(db.Integer, db.ForeignKey('userdata_table.id'))
    products = db.relationship('ProductsInOrder',
                               backref='order',
                               lazy='dynamic')

    def __init__(self, total, user_id, address):
        self.total = total
        self.user_id = user_id
        self.date = datetime.utcnow()
        self.address = address

    def __repr__(self):
        return "<Order(%r)>" % self.total


class ProductsInOrder(db.Model):

    __tablename__ = "products_in_order_table"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product_table.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order_table.id'))
    product = db.relationship('Product')

    def __init__(self, product_id, order_id, quantity):
        self.product_id = product_id
        self.order_id = order_id
        self.quantity = quantity

    def __repr__(self):
        return "<ProductsInOrder(%r)>" % self.product_id


class ShippingMethods(db.Model):
    __tablename__ = 'shipping_methods_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    deliveryTime = db.Column(db.Float, nullable=False)
    area = db.Column(db.String, nullable=False)

    def __init__(self, name, price, delivery_time, area):
        self.name = name
        self.price = price
        self.deliveryTime = delivery_time
        self.area = area

    def __repr__(self):
        return "ShippingMethods(%r)" % self.name










	
