""" Usage:
    <file-name> --db=DB_FILE --query=QUERY_FILE --out=OUTPUT_FILE [--debug]
"""
# Set default encoding to utf8
import sys
reload(sys) 
sys.setdefaultencoding('UTF8')

# External imports
import logging
from pprint import pprint
from pprint import pformat
from docopt import docopt

from sqlite_manager import Sqlite_Database
import sys

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    db_fn = args["--db"]
    query_fn = args["--query"]
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    with Sqlite_Database(db_fn) as db:
        query = " ".join([line.strip()
                          for line in open(query_fn)])
        logging.info("Running: {}".format(query))
        result = db.conn.execute(query).fetchall()

    logging.info("Writing result to {}".format(out_fn))

    with open(out_fn, 'w') as fout:
        fout.write("\n".join(["\t".join(map(str, fields))
                              for fields in result]).encode("utf8"))


    # print("counting venues before 2000...")
    # unique_venues_before = db.conn.execute(" \
    # SELECT DISTINCT venue  \
    # FROM papers WHERE year <= 2000 ;\
    # ").fetchall()

    # pby = db.conn.execute(" \
    # SELECT year,COUNT(DISTINCT venue)  \
    # FROM papers \
    # GROUP BY year \
    # ORDER BY year; \
    # ").fetchall()


#    print("#unique venues = {}".format(unique_venues))

    # print("counting venues after 2000...")
    # unique_venues = db.conn.execute("SELECT count(distinct venue) FROM papers WHERE year > 2000 ;").fetchall()x
    # print("#unique venues = {}".format(unique_venues))
