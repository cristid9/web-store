## @package cart
#  This module contains the implementation of the \ref Cart
#  object and implementations of different objects related
#  to a cart.

from main import db
from flask import session
from product import Product
from datetime import datetime

## This class represents the cart of an user.
class Cart(object):
    def __init__(self, cart, shipping):
        self.items = cart
        self.shipping = float(shipping)

    ## Use this method to add a new product to the cart.
    #
    #  @param productId The id of the product that will be
    #         added to the cart.
    #  @param price The price of the product that will be
    #         added to the cart.
    #
    # @return void It doesn't return anything.
    def addToCart(self, productId, price):
        self.items[productId] = {
            "price": price,
            "quantity": 1
        }

    ## Use this method to check if the cart is empty.
    #
    # @return void It doesn't return anything.
    def is_empty(self):
        return not bool(self.items)

    ## Use this method to delete a product from the cart.
    #
    # @return void It doesn't return anything.
    def deleteFromCart(self, productId):
        del self.items[productId]

    ## Use this method to update the quantity of a product
    #  in cart.
    #
    # @return void It doesn't return anything.
    def updateQuantity(self, productId, newQuantity):
        self.items[productId]["quantity"] = newQuantity

    ## Use this method to get the sum of the prices of the
    #  products in the cart.
    #
    # @return int The sum of the products in the cart.
    def getTotal(self):
        total = 0
        for item in self.items:
            total += self.items[item]["quantity"] * \
                     self.items[item]["price"]
        return total + float(self.shipping)

    ## Because I can't perform queries from templates I need
    #  a list with all products bought by the user.
    #
    # @return void It doesn't return anything.
    def getProductData(self):
        data = []
        for product_id in self.items:
            data.append(Product.query.get(product_id))

        return data

    ## Use this method to change the shipping method chosed
    #  by the user.
    #
    # @param price The price of the new shipping method.
    #
    # @return void It doesn't return anything.
    def updateShipping(self, price):
        self.shipping = price

    ## Use this method to get the ids of all the products in
    #  cart.
    #
    # @return list A list cotaining the id of all the products
    #         in the cart.
    def get_products_ids(self):
        return self.items.keys()

    ## Use this method to get the quantity of a product in the
    #  cart by its id.
    #
    # @return int The quantity of the product matching that id.
    def get_quantity_by_id(self, product_id):
        return self.items[product_id]["quantity"]


## Represents an order. Usually, an order is log of the items
#  bought by an user at a given time.
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


## There can be many products in an order. The only way we
#  can bind the products in the order to the order is using
#  a one(order) to many(products) relationship. The purpose
#  of this class is to fulfil this purpose.
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

## Class used to represent a shipping method.
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
