""" Usage:
    <file-name> --db=DB_FILE --json=JSON_FILE [--debug]
"""
# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
import sqlite3
from tqdm import tqdm

# Local imports
from sqlite_manager import Sqlite_Database
from add_gender import lazy_paper_reader
#=-----

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    db_fn = args["--db"]
    json_fn = args["--json"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    with Sqlite_Database(db_fn) as db:
        for paper in tqdm(lazy_paper_reader(json_fn)):
            json_genders = [author['gender']
                            for author
                            in paper['authors']]
            json_authors = [author['name']
                            for author
                            in paper['authors']]

            db_genders, db_authors = db.get_paper_genders(paper['id'])

            assert(db_genders == json_genders)
            assert(db_authors == json_authors)

        logging.info("DONE")
