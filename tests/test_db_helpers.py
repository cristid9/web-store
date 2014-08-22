from src.app.db.helpers import equals, notEquals, lessThan, greaterThan,\
								lessOrEquals, greaterOrEquals, And
import unittest

class TestDBHelpers(unittest.TestCase):
	def test_equals(self):
		expectedValue = ('a = %(a)s', {'a': '12'})
		self.assertEqual(expectedValue, equals('a', 12))
	
	def test_notEquals(self):
		expectedValue = ('a != %(a)s', {'a': '12'})
		self.assertEqual(expectedValue, notEquals('a', 12))

	def test_lessThan(self):
		expectedValue = ('a < %(a)s', {'a': '1'})
		self.assertEquals(expectedValue, lessThan('a', 1))		

	def test_greaterThan(self):
		expectedValue =	 ('a > %(a)s', {'a': '12'}) 
		self.assertEquals(expectedValue, greaterThan('a', 12))		

	def test_lessOrEquals(self):
		expectedValue = ('a <= %(a)s', {'a': '12'})
		self.assertEquals(expectedValue, lessOrEquals('a', 12))

	def test_greaterOrEquals(self):
		expectedValue = ('a >= %(a)s', {'a': '12'})
		self.assertEquals(expectedValue, greaterOrEquals('a', 12))

	def test_And(self):
		expectedValue = ('AND a = %(a)s', {'a': 12})
		self.assertEquals(expectedValue, And(("a = %(a)s", {"a": 12})))
