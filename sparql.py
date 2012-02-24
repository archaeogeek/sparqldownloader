import sys

from SPARQLWrapper import SPARQLWrapper, JSON

from Required import ConfigParse

class Sparql():

	def __init__(self):
		
		
		# generic config
		opts = ConfigParse.OptParser()
		self.filename = opts.filename
		self.endpoint = opts.endpoint
		print self.endpoint

	def CreateTable(self, tablename, fields):
	## database table creation function - needs editing for this script
		fieldslist = ",".join([' %s %s' % (key, value) for key, value in fields.items()])

		try:
			sCreateSQL = 'CREATE TABLE %s (%s)' % (tablename, fieldslist)
			#print sCreateSQL
			self._conn.query(sCreateSQL)
			self.out.OutputInfo("Table %s created." % tablename)
		except:
			self.out.OutputError("Could not create %s. Script aborting"  % tablename)
			sys.exit(1)

	def sparqldownload(self):

		#read contents of sparql.txt into a variable for passing to endpoint
		querystring = open(self.filename, 'r').read()
		try:
			sparql = SPARQLWrapper(self.endpoint)
			sparql.setQuery(querystring)
			sparql.setReturnFormat(JSON)
			results = sparql.query().convert() #returns a dictionary

			for result in results["results"]["bindings"]: #returns a list where key is a single item and value is a dictionary
    				for key,value in result.items():
					print key #this would provide the columns for the table
					print value['value'] #this provides the data for the table
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

