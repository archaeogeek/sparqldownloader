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
from optparse import OptionParser
from Required import Data, OutPut, TextClean, ConfigParse


class Sparql():

    def __init__(self):

        desc = """Download linked data from sparql endpoint using a valid sparql query provided as a text file.
        Usage: sparql.py -f filename -e endpoint -c config"""
        parser = OptionParser(description=desc)
        parser.add_option("-f","--file", dest="filename", help="location of sparql query file (mandatory)")
        parser.add_option("-e","--endpoint", dest="endpoint", help="location of sparql endpoint (mandatory)")
        parser.add_option("-c","--config", dest="config", help="location of config file (mandatory)")
        (options, args) = parser.parse_args()

        mandatories = ['filename', 'endpoint', 'config']
        for m in mandatories:
            if not options.__dict__[m]:
                    print "a mandatory option is missing"
                    parser.print_help()
                    exit(-1)

        self.options = options
        self.filename = options.filename
        self.endpoint = options.endpoint
        self.config = options.config

        # get today's date for naming log file
        now = date.today()
        self.dateStr = now.isoformat()

        #Output to log file
        opts = ConfigParse.ConfParser()
        outputcreds = opts.ConfigSectionMap('Output')
        self.outputlevel = outputcreds['outputlevel']
        self.out = OutPut.ClassOutput('Sparql')

        #Text cleanup
        self.textclean = TextClean.ClassTextClean(self.out)

        # database connection from config.ini
        conf = ConfigParse.ConfParser()
        dbcreds = conf.ConfigSectionMap('DatabaseConnection')
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
            if self.outputlevel == 'INFO':
                self.out.SetOutputLevel(OutPut.OUTPUTLEVEL_INFO)
            elif self.outputlevel == 'ERROR':
                self.out.SetOutputLevel(OutPut.OUTPUTLEVEL_ERROR)
            else:
                self.out.SetOutputLevel(OutPut.OUTPUTLEVEL_DEBUG)
            self.out.SetFileLogging(True)
            self.out.OutputInfo('___________________________')
            self.out.OutputInfo('Sparql Download starting')
            print "Got here OK"
            self.out.OutputInfo('Endpoint: %s' % self.endpoint)
            self.out.OutputInfo('Query: %s' % self.filename)
        except:
            self.ExtraErrorHandling()

        try:
            self._conn = self._Data.OpenPostgres()
        except:
            print "I cannot connect to the supplied database"
            self.out.OutputError("Problem connecting to database %s." % self.dbname)
            self._Data.ClosePostgres()
            sys.exit(1)

        #read contents of sparql.txt into a variable for passing to endpoint-
        #use filename as name for database table
        # need to do some text validation (use text cleanup)
        try:
            querystring = open(self.filename, 'r').read()
        except:
            self.out.OutputError('File %s does not exist. Script aborting' % self.filename)
            self._Data.ClosePostgres()
            sys.exit(1)

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
            results = sparql.query().convert()  # returns a dictionary
        except:
            self.ExtraErrorHandling()

        try:
        #extract bits we want from results and convert into table in database
            firstLoop = True
            for result in results["results"]["bindings"]:
                if firstLoop:
                    for key, value in result.items():
                        fieldlist[key] = 'varchar'
                    self._Data.CreateTable(tablename, fieldlist)
                    firstLoop = False
                else:
                    for key, value in result.items():
                        val = self.textclean.Cleanup(value['value'])
                        val = "'" + val + "'"
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
    except (KeyboardInterrupt):
        print "Keyboard interrupt detected. Script aborting"
        raise
    except:
        sys.exit(1)

if __name__ == "__main__":
    main()
