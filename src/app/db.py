## @package db
#
#  The purpose of this module is to provide basic functionality to do basic
#  queries to the aplication's database/

import psycopg2


## Provides methods for connecting to the database and making queries. All the
#  classes related to a parcitular component of the system will call methods 
#  provided byt this class to make queries to the database.
class DB(object):
	
	## Consructor method of the DB class.
	def __init__(self, dbName, dbUser, dbPassword, dbPort, dbHost):
		self.conn = psycopg2.connect(
			database=dbName,
			user=dbUser,
			password=dbPassword,
			host=dbHost,
			port=dbPort
		)
	
		self.cur = self.conn.cursor()
		

	## Generic method used to insert a set of values into a given database.
	#
	#  @param **kwargs Should contain pairs of the form <field>: <value> and
	#         it is verry important to contain the `table` key. The table key
	#         will specify the able from the database where the datas should be
	#         inserted.
	#
	#  @return None Doesn't return anything.
	def insertRecord(self, **kwargs):
		if 'table' not in kwargs.keys()
			pass # raise an error


		table = kwargs['table']
		del kwargs['table']

		query_fields = kwargs.keys()
		pg_fields = []

		for field in query_fields:
			pg_fields.append('%(' + field + ')')
		
		query_field_string = ', '.join(query_fields)
		query_pg_string = ', '.join(pg_field)
		
		self.cur.execute('INSERT INTO ' + table + '(' + 
			query_field_string + ') VALUES (' + query_pg_string + ')',
			kwargs
		 )
	
		self.conn.commit()

	def __del__(self):
		pass
