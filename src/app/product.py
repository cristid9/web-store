## @package product
#
#  This module contains the implementation of the \ref Product
#  class and of different classes related to \ref Product.

from main import db
from datetime import datetime

## Used to represent an product.
class Product(db.Model):
    __tablename__ = 'product_table'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    # When we delete a product we actually make is unavailable, thus
    # keeping the integrity of all the references to that product, like
    # orders, for example.
    available = db.Column(db.Boolean, nullable=False, default=True)

    comments = db.relationship('ProductComment', backref='product',
                               lazy='dynamic')

    pictures = db.relationship('ProductPictures', backref='product',
                               lazy='dynamic')

    specifications = db.relationship('ProductSpecifications',
                                     backref='product',
                                     lazy='dynamic')

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
        self.date = datetime.utcnow()

    def __repr__(self):
        return "<Product(%r, %r, %r)>" % (self.name, self.price, self.stock)


## Use to represent the pictures of a product.
class ProductPictures(db.Model):
    __tablename__ = "product_pictures_table"

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('product_table.id'))

    def __init__(self, link, productId):
        self.link = link
        self.productId = productId
        self.date = datetime.utcnow()

    def __repr__(self):
        return "<ProductPicures(%r)>" % self.link


## Used to represent the comments of an product.
class ProductComment(db.Model):
    __tablename__ = 'product_comments_table'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    productId = db.Column(db.Integer, db.ForeignKey('product_table.id'))
    user = db.relationship('User')

    def __init__(self, comment, userId):
        self.comment = comment
        self.userId = userId
        self.date = datetime.utcnow()

    def __repr__(self):
        return "<ProductComment(%r)>" % self.comment


## Used to represent the categories that a product can belong
#  to.
class Categories(db.Model):
    __tablename__ = 'categories_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    # If we delete delete all the products in a category, it doesn't
    # make any sense to keep that category available, since there are
    # no products in it.
    available = db.Column(db.Boolean, nullable=True, default=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Categories(%r)" % self.name


## Used to represent the specifications of a product.
class ProductSpecifications(db.Model):
    __tablename__ = 'product_specification_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    data = db.Column(db.String, nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('product_table.id'))

    def __init__(self, productId, name, data):
        self.productId = productId
        self.name = name
        self.data = data

    def __repr__(self):
        return "ProductSpecfication(%r)" % self.name
