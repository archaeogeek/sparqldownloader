# Sparqldownloader

Python script that takes a valid sparql query (that delivers a tabular result), and a valid endpoint, and downloads the result into a PostgreSQL database.

Tested with python 2.6 but should/may work with 2.5+. Should work with windows and linux variants- not tested with Mac.

**Requirements**

  - Python 2.5+
  - PostgreSQL 8.x +
  - PygreSQL for your version of python- get it [here](http://http://www.pygresql.org/)
  
 **Instructions**

  - Edit the supplied config.ini.sample to match your database credentials (host, username, password, port, database name), and choose a logging level from the supplied options.  Save it as config.ini.
  - Construct a valid sparql query that returns tabular data and save it as a text file in the root sparqldownloader directory. The python script will use the name of the text file for the name of the table. Some sample scripts are provided in the samples directory, with valid endpoints provided in the comments at the top of each file.
  - Copy the URL for an appropriate sparql endpoint
  - Use at the command line as below, using the full path to your python executable if required. If you have multiple python installations, ensure that you use the one with pygresql installed.
  - Log files can be found in the Logs directory, please clear this out periodically as (at present) there are no methods of automatically removing old logs.

**Usage**

    python sparql.py -f filename -e endpoint -c config

Where:

  - f is the name of a text file containing the sparql query

  - e is the URL for a valid endpoint

  - c is a config.ini file containing database credentials and error reporting level

  **Caveats**

  This was done to scratch an itch and teach myself further python. As such it's fairly rudimentary! Given time I will improve the code and may add additional functionality as necessary. The examples are mainly UK-oriented, and gathered from various locations on the internet- the authors are acknowledged in the comments at the top of each file.
  


  