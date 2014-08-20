## @package db
#
#
#
#

import psycopg2

class Db(object):
	
	def __init__(self, dbName, dbUser, dbPassword, dbPort, dbHost):
		self.conn = psycopg2.connect(
			database=dbName,
			user=dbUser,
			password=dbPassword,
			host=dbHost,
			port=dbPort
		)
	
		self.cur = self.conn.cursor()
		

	def insertRecord(**kwargs):
		pass

	def __del__(self):
		pass
