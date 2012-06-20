# -*- coding: utf8 -*-

#for python 2.5
#2.7 includes json

## Copyright (c) 2011 Astun Technology

## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.

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
					self._Data.CreateTable(tablename, fieldlist)
					firstLoop = False
				else:
					for key,value in result.items():
						val = self.textclean.Cleanup(value['value'])
						val = "'" + val + "'"	#need to wrap in quotes to deal with spaces
						dbdata[key] = val
					self._Data.InsertTable(dbdata, tablename) 
		except:
			self.ExtraErrorHandling()
		finally:
			self._Data.ClosePostgres()
			print 'Sparql Download completed'
		return
		

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

