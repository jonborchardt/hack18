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
from sqlite_manager import paper_int_id
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


    conn = sqlite3.connect(db_fn)

    for paper in tqdm(lazy_paper_reader(json_fn)):
        db_genders_ls = conn.execute("select (author_gender) FROM papers where paper_id='{}'".format(paper_int_id(paper["id"]))).fetchall()
        assert(len(db_genders_ls) == 1)

        db_genders = db_genders_ls[0][0].split(';;;')
        json_genders = [author['gender']
                        for author
                        in paper['authors']]
        assert(db_genders == json_genders)
    logging.info("DONE")
