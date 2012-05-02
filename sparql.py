import sys
import os
from datetime import date
from SPARQLWrapper import SPARQLWrapper, JSON
from Required import ConfigParse, Data, OutPut,TextClean

class Sparql():

	def __init__(self):

		# get today's date
		now = date.today()
		self.dateStr = now.isoformat()
		
		
		# generic config
		opts = ConfigParse.OptParser()
		self.filename = opts.filename
		self.endpoint = opts.endpoint

		#Output to log file
		self.out = OutPut.ClassOutput('Sparql')
		
		#cleanup
		self.textclean = TextClean.ClassTextClean(self.out)

		# generic database connection stuff #needs sorting for this script
		dbcreds = opts.ConfigSectionMap('DatabaseConnection')
		self._Data = Data.ClassData(self.out)
		self.host = dbcreds['host']
		self.username = dbcreds['username']
		self.password = dbcreds['password']

	def ExtraErrorHandling(self):
		'''generic function for printing error message before exiting script'''
		e = sys.exc_info()[1]
		print "Error: %s" % e 
		sys.exit(1)

	def DoesTableExist(self, table):
		'''generic function to check if a table exists or not'''
		sSQL = "SELECT relname from pg_class WHERE relname = '%s'" % table
		q = self._conn.query(sSQL)
		return q.getresult()

	def DropTable(self, tablename):
		''' generic function for dropping a database table called [tablename]'''
		res = self.DoesTableExist(tablename)
		if res:
			sDropSQL = 'DROP TABLE %s' % tablename
			try:
				self._conn.query(sDropSQL)
			except:
				self.out.OutputError("There was a problem dropping table %s." % tablename)
		else:
			pass #if it doesn't exist we don't need to drop it
	
	def CreateTable(self, tablename, fieldlist):
		'''generic function to create database table from fields provided as a dictionary'''

		sAggSQL = "SELECT relname from pg_class WHERE relname = '%s'" % tablename
		q_agg = self._conn.query(sAggSQL)
		res_agg = q_agg.getresult()
		if not res_agg:
			self.out.OutputInfo("No previous version of %s exists." % tablename)
		else:
			sAlterSQL = "ALTER TABLE %s RENAME TO %s_prev" % (tablename, tablename)
			try:
				self.DropTable('%s_prev' % tablename)
				self._conn.query(sAlterSQL) 
			except:
				self.out.OutputError("Could not rename %s" % tablename)
 		
		fields = ",".join([' %s %s' % (key, value) for key, value in fieldlist.items()])
		try:
			sCreateSQL = 'CREATE TABLE %s (%s)' % (tablename, fields)
			print sCreateSQL
			self._conn.query(sCreateSQL)
			self.out.OutputInfo("Table %s created." % tablename)
		except:
			self.out.OutputError("Could not create table %s. Script aborting"  % tablename)
			self.ExtraErrorHandling()

	def InsertTable(self, dbdata, table):
		'''generic function for inserting data from a dictionary into a table'''
		fvals = ', '.join(dbdata.values())
		fkeys = ', '.join(dbdata.keys())
		sInsertSQL = "INSERT INTO %s (%s) VALUES (%s)" % (table, fkeys, fvals)
		try:
			self._conn.query(sInsertSQL.encode('utf8'))
		except:
			self.out.OutputError("No data entered into %s" % table)
			self.ExtraErrorHandling()

	def sparqldownload(self):

		try:
			#set up logging
      			self._sName = '%s_Sparql' % self.dateStr
      			self.out.SetFilename( self._sName + '.log' )
      			self.out.SetOutputLevel(OutPut.OUTPUTLEVEL_INFO)
      			self.out.SetFileLogging( True )
      			self.out.OutputInfo('___________________________')
      			self.out.OutputInfo('Sparql Download starting')
		except:
			self.ExtraErrorHandling()
		
		try:
			self._conn = self._Data.OpenPostgres()
		except:
			print "I cannot connect to the supplied database"
			self.out.OutputError("Problem connecting to database %s." % self.dbname) 
			self._Data.ClosePostgres()
			sys.exit(1)

		#read contents of sparql.txt into a variable for passing to endpoint- use filename as name for database table
		# need to do some text validation (use text cleanup)
		querystring = open(self.filename, 'r').read()

		#get filename without extension as table name
		base = os.path.basename(self.filename)
		tablename = os.path.splitext(base)[0]
		
		#create a temporary dictionary to hold field names
		fieldlist = dict()
		dbdata = dict()

		try:
		#do sparql magic and return dictionary of results
			sparql = SPARQLWrapper(self.endpoint)
			sparql.setQuery(querystring)
			sparql.setReturnFormat(JSON)
			results = sparql.query().convert() #returns a dictionary
		except:
			self.ExtraErrorHandling()

		try:
		#extract bits we want from dictionary of results and convert into table in database
			firstLoop = True
			for result in results["results"]["bindings"]: #returns a list where key is a single item and value is a dictionary
				if firstLoop:
    					for key,value in result.items():
						fieldlist[key] = 'varchar' #append key to dict with value varchar to create column list
					self.CreateTable(tablename, fieldlist)
					firstLoop = False
				else:
					for key,value in result.items():
						val = self.textclean.Cleanup(value['value'])
						val = "'" + val + "'"	#need to wrap in quotes to deal with spaces
						dbdata[key] = val
					self.InsertTable(dbdata, tablename) 
		except:
			self.ExtraErrorHandling()
		

def main():
	
	try:
 		gothunderbirdsgo = Sparql()
		gothunderbirdsgo.sparqldownload()
	except (KeyboardInterrupt, SystemExit):
		print "Keyboard interrupt detected. Script aborting"
        	raise
	except:
		sys.exit(1)

if __name__ == "__main__":
	main()

