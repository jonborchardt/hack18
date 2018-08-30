""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]
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

# Local imports

#=-----

class sqlite_database:
    """
    Sqlite3 interface.
    """

    def __init__(self, db_filename):
        """
        Store filename.
        """
        self.db_filename = db_filename

    def __enter__(self):
        """
        Open sqlite connection and set up tables.
        """
        self.conn = sqlite3.connect(self.db_filename)
        self.conn.execute('CREATE TABLE papers (paper_id TEXT, author_name TEXT, author_gender TEXT)')
        return self

    def add_paper(self, paper):
        """
        Add a paper to db.
        """
        paper_id = paper['id']
        for author in paper['authors']:
            # command = "INSERT INTO papers (paper_id, author_name, author_gender) VALUES ('{paper_id}', '{author_name}', '{author_gender}')"\
            #           .format(paper_id = paper_id,
            #                   author_name = author['name'],
            #                   author_gender = author['gender'])
#            logging.info(command)
            self.conn.execute("INSERT INTO papers (paper_id, author_name, author_gender) VALUES (?, ?, ?)",
                              (paper_id,
                               author['name'],
                               author['gender']))


    def __exit__(self, *args):
        """
        Close this instance and commit to file.
        """
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    logging.info("DONE")
