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
import math

# Local imports

#=-----


def paper_int_id(paper_id):
    """
    Get a unique integer for the given input string paper_ind
    """
    return hash(paper_id)

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
        self.conn.execute('CREATE TABLE papers (paper_id INTEGER PRIMARY KEY, author_name TEXT, author_gender TEXT)')
        return self

    def add_paper(self, paper):
        """
        Add a paper to db.
        """
        paper_id = paper_int_id(paper['id'])
        authors = paper['authors']
        names = ";;;".join([author['name']
                             for author
                             in authors])
        genders = ";;;".join([author['gender']
                              for author
                              in authors])

        self.conn.execute("INSERT INTO papers (paper_id, author_name, author_gender) VALUES (?, ?, ?)",
                          (paper_id,
                           names,
                           genders))


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

    paper_ids = ["23e8d287dac954af1b421fba69bc0158541563c0",
                 "32ac51549382a64551ccfe55bf2315362c8a42e0",
                 "cfa06e42e057801131f757d7e520c39b6893a83a"]

    assert(len(set(map(paper_int_id, paper_ids))) == len(paper_ids))

    logging.info("DONE")
