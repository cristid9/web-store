from src.app.db.helpers import equals, notEquals, lessThan
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
