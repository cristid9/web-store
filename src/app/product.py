## @package product
#
#
#
#

##
#
#
#
class Product(object):
	
	def __init__(self, db, product_id):
		self.db = db
		self.name = None
		self.pictures = None
		self.price = None
		self.availability = None
		self.comments = None
		self.product_id = None
	
	@staticmethod
	def addProduct(self, name, pictures, price, stock):
		# Add product to the products table
		pass

	@staticmethod
	def deleteProduct(self, product_id):
		pass

	def loadProduct(self, product_id):
		pass

	def addProductCommnet(self, comment):
		pass

	def paginateComments(self):
		pass
