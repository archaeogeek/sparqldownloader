# Sparqldownloader

Python script that takes a valid sparql query (that delivers a tabular result), and a valid endpoint, and downloads the result into a PostgreSQL database.

Tested with python 2.6 but should/may work with 2.5+.

**Requirements**

  - Python 2.5+
  - PostgreSQL 8.x +
  - PygreSQL for your version of python- get it here: 
  
 **Instructions**

  - Edit the supplied config.ini.sample to match your database credentials (host, username, password, port, database name) and save it as config.ini
  - _

**Usage**

    python sparql.py -f filename -e endpoint -c config

Where:

  - f is the name of a text file containing the sparql query

  - e is the URL for a valid endpoint

  - c is a config.ini file containing database credentials and error reporting level
  


  