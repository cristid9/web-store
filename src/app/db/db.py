## @package db
#
#  The purpose of this module is to provide basic functionality to do basic
#  queries to the aplication's database/

import psycopg2


## Provides methods for connecting to the database and making queries. All the
#  classes related to a parcitular component of the system will call methods 
#  provided byt this class to make queries to the database.
class DB(object):
	## Dockblock here
	INSERT = 1
	DELETE = 2
	UPDATE = 3
	SELECT = 4

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
		
		## Dockblock here
		self.dbQuery = None
		## Dock block here
		self.dbQueryType = None

	## Generic method used to insert a set of values into a given database.
	#
	#  @param **kwargs Should contain pairs of the form <field>: <value> and
	#         it is verry important to contain the `table` key. The table key
	#         will specify the able from the database where the datas should be
	#         inserted.
	#
	#  @return Nonei Doesn't return anything.
	def insertRecord(self, table, **kwargs):
		query_fields = sorted(kwargs.keys())
		pg_fields = []

		for field in query_fields:
			pg_fields.append('%(' + field + ')s')
		
		query_field_string = ', '.join(query_fields)
		query_pg_string = ', '.join(pg_fields)
		
		self.dbQuery = ('INSERT INTO ' + table + '(' + 
			query_field_string + ') VALUES (' + query_pg_string + ')',
			kwargs
		)

		self.dbQueryType = self.INSERT

		return self
	
	## Dockblock here
	#
	#
	#
	#
	def select(self, table, *args):
		query = "SELECT " + ", ".join(sorted(args)) + " FROM " + str(table)
		self.dbQuery = (query, {})
		self.dbQUeryType = self.SELECT

		return self

	## Dockblock here
	#
	def where(self,	*conditions):	
		self.dbQuery = list(self.dbQuery)
		self.dbQuery[0] += " WHERE " +\
			 " ".join(query for query, dct in list(conditions))
		
		# Now let's merge the dicts with the parameters
		dictBig = {}
		for query, dct in conditions:
			dictBig.update(dct)

		self.dbQuery[1].update(dictBig)
		self.dbQuery = tuple(self.dbQuery)
		
		return self


	## Dockblock here
	#
	#
	#
	def perform(self):
		self.cur.execute(*self.dbQuery)
		
		if self.dbQueryType != self.SELECT:
			self.conn.commit()
	
	##
	#
	#
	#
	#
	#
	def update(self, table, **kwargs):
		query = 'UPDATE ' + table + ' SET '
		query += ", ".join(key + '=%(' + key + ')s' for key in kwargs.keys())
		
		self.dbQuery = (query, kwargs)
		self.dbQueryType = self.UPDATE

		return self

	##
	#
	#
	#
	#
	def deleteFrom(self, table):
		query = "DELETE FROM " + table 

		self.dbQuery = (query, {})
		self.dbQueryType = self.DELETE

		return self
		
	def __del__(self):
		pass
