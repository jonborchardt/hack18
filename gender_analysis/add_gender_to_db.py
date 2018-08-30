""" Usage:
    add_gender --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

Add a gender column to the an S2 input file (json lines), output written to a
new *sqlite* file.
"""
# Set default encoding to utf8
import sys
reload(sys) 
sys.setdefaultencoding('UTF8')

# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
from tqdm import tqdm
import json
import sqlite3

# Local imports
from add_gender import lazy_paper_reader
from sqlite_manager import sqlite_database
#=-----

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

    # Load input file
    logging.info("Adding gender...")
    paper_cnt = 0

    with sqlite_database(out_fn) as db:
        for paper in tqdm(lazy_paper_reader(inp_fn)):
            paper_cnt += 1
            db.add_paper(paper)

    logging.info("Wrote {} papers to {}".format(out_fn,
                                                paper_cnt))
    logging.info("DONE")
