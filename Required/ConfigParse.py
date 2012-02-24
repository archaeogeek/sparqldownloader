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

### ConfigParse.py - Class to parse a configuration file and return results back to python script

# import modules
import ConfigParser
from optparse import OptionParser

class OptParser():

	def __init__(self):
		desc ="""Download data sparql endpoint. """
		parser=OptionParser(description = desc)
		parser.add_option("-f","--file", dest="filename", help="location of sparql query file (mandatory)")
		parser.add_option("-e","--endpoint", dest="endpoint", help="location of sparql endpoint (mandatory)")
		(options, args) = parser.parse_args()

		mandatories = ['filename','endpoint']
		for m in mandatories:
   			if not options.__dict__[m]:
        			print "a mandatory option is missing"
        			parser.print_help()
        			exit(-1)

		self.options = options
		self.filename = options.filename
		self.endpoint = options.endpoint












