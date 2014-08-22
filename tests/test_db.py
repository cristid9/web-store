import unittest
from src.app.db import DB

class TestDB(unittest.TestCase):
	def setUp(self):
		self.dbConn = DB(dbName='test_web_store_db',
			dbUser='cristi',
			dbPassword='1234',
			dbHost='localhost',
			dbPort=5432 
		)	
		self.dbCur = self.dbConn()

	def tearDown(self):
		self.dbConn.close()
		self.dbCur.close()
