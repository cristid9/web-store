## @package user
#
#
#
#

##
#
#
#
class User(object):
	
	##
	#
	#
	#
	def __init__(self, db=None, user_id=None):
		self.db = db
		self.username = None
		self.email = None
		self.state = None
		self.user_id = user_id
		self.loadUser(user_id)

	@staticmethod
	def addUser( username, password, email):
		# Add query to add a new record in the user table
		pass

	def loadUser(self, user_id):
		# Add query to load a user from the database
		pass

	@staticmethod	
	def deleteUser(user_id):
		# Delete a user using it's id
		pass
			
