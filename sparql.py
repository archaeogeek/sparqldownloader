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
		print self.endpoint

		#Output to log file
		self.out = OutPut.ClassOutput('Sparql')
		
		#cleanup
		self.textclean = TextClean.ClassTextClean(self.out)


		# generic database connection stuff #needs sorting for this script
		try:
			dbcreds = opts.ConfigSectionMap('DatabaseConnection')
			self._Data = Data.ClassData(self.out)
			self.host = dbcreds['host']
			self.username = dbcreds['username']
			self.password = dbcreds['password']
			print self.username
		except:
			e = sys.exc_info()[1]
			print "Error: %s" % e 
			sys.exit(1)

	def DropTable(self, tablename):
	## database table dropping function
		sDropSQL = 'DROP TABLE %s' % tablename
		try:
   			self._conn.query(sDropSQL)
			self.out.OutputInfo("The table %s has been successfully dropped." % tablename)
		except:
   			self.out.OutputInfo("Table %s does not exist, so cannot be dropped." % tablename)

	def CreateTable(self, tablename, fieldlist):
	## database table creation function

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
			e = sys.exc_info()[1]
			print "Error: %s" % e 
			self.out.OutputError("Could not create %s. Script aborting"  % tablename)
			sys.exit(1)

	def InsertTable(self, dbdata, table):
	## inserts json dictionary values into table, or updates existing - needs editing for this script
		try:
			fvals = ', '.join(dbdata.values())
			fkeys = ', '.join(dbdata.keys())

		except:

			e = sys.exc_info()[1]
			print "Error: %s" % e 
			sys.exit(1)

		sInsertSQL = "INSERT INTO %s (%s) VALUES (%s)" % (table, fkeys, fvals)
		print sInsertSQL

		try:
		
			self._conn.query(sInsertSQL.encode('utf8'))
		except:
			self.out.OutputError("No data entered into %s" % table)
			e = sys.exc_info()[1]
			print "Error: %s" % e 
			sys.exit(1)

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
			e = sys.exc_info()[1]
			print "Error: %s" % e 
			sys.exit(1)
		
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
		
		#create a temp list to hold field names
		fieldlist = dict()
		dbdata = dict()

		try:
		#do sparql magic and return dictionary of results
			sparql = SPARQLWrapper(self.endpoint)
			sparql.setQuery(querystring)
			sparql.setReturnFormat(JSON)
			results = sparql.query().convert() #returns a dictionary

		except:
			e = sys.exc_info()[1]
   			print "Error: %s" % e 
			sys.exit(1)
		try:
		#extract bits we want from dictionary of results and convert into table in database
			firstLoop = True
			for result in results["results"]["bindings"]: #returns a list where key is a single item and value is a dictionary
				if firstLoop:
    					for key,value in result.items():
						fieldlist[key] = 'varchar' #append key to dict with value varchar to create column list
					self.CreateTable(tablename, fieldlist)
					firstLoop = False
					print "first iteration done"
				else:
					print "into second iteration"					
					for key,value in result.items():

						val = self.textclean.Cleanup(value['value'])
						val = "'" + val + "'"	#need to wrap in quotes to deal with spaces
						dbdata[key] = val
					self.InsertTable(dbdata, tablename) #this only inserts one value at the moment- needs to loop
			

		except:
			e = sys.exc_info()[1]
   			print "Error: %s" % e 
			sys.exit(1)
		

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

