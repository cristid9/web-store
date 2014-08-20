## @package db
#
#
#
#

import psycopg2

class Db(object):
	
	def __init__(self, dbName, dbUser, dbPassword, dbPort, dbHost):
		psycopg2.connect(
			database=dbName,
			user=dbUser,
			password=dbPassword,
			host=dbHost,
			port=dbPort
		)

	def insertRecord(**kwargs):
		pass

	def __del__(self):
		pass
