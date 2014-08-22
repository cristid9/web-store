import unittest
from src.app.db import DB

class TestDB(unittest.TestCase):
	def setUp(self):
		self.db = DB(dbName='test_web_store_db',
			dbUser='cristi',
			dbPassword='1234',
			dbHost='localhost',
			dbPort=5432 
		)	


