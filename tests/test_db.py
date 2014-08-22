import unittest
from src.app.db.db import DB

class TestDB(unittest.TestCase):
	def setUp(self):
		self.db = DB(dbName='test_web_store_db',
			dbUser='cristi',
			dbPassword='1234',
			dbHost='localhost',
			dbPort=5432 
		)	

	def test_insertValue(self):
		self.db.insertRecord('test', col1='val1', col2='val2')
		args = sorted(['col1', 'col2'])
		queryString = ("INSERT INTO test({0}, {1}) VALUES (%({0})s, "\
			+ "%({1})s)").format(*args)
		
		expectedValue = (queryString, {
				"col1": "val1",
				"col2": "val2"
			}
		)
		
		self.assertEqual(self.db.dbQuery, expectedValue) 

	def test_select(self):
		self.db.select('test', 'col1', 'col2')
		
		queryString = "SELECT col1, col2 FROM test"
		expectedValue = (queryString, {})

		self.assertEqual(self.db.dbQuery, expectedValue)

	def test_where(self):
		self.db.dbQuery = ("", {})
		self.db.where(("a = %(a)s", {"a": 2}), ("AND b = %(b)s", {"b": 2}))
	
		expectedValue = (" WHERE a = %(a)s AND b = %(b)s", {
				"a": 2,
				"b": 2
			}
		)
			
		self.assertEqual(self.db.dbQuery, expectedValue)





