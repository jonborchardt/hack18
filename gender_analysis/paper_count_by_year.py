""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

Answer:

1. Is the number (proportion) of female authors increasing?
2. Is the number (proportion) of female first authors increasing?
6. Bechedel
"""
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
import json
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
from count_alphabetical import is_alphabetical

# Local imports
from add_gender import lazy_paper_reader
#=-----

from collections import namedtuple

year_record = namedtuple("YearRecord",
                         ["total",
                          "first_author",
                          "last_author"])

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

    paper_by_year = defaultdict(lambda: 0)


    for paper in tqdm(lazy_paper_reader(inp_fn)):
        cur_authors = paper["authors"]

        # add first and last author stats -- only for non-alphabetical
        if cur_authors:
            paper_by_year[paper["year"]] += 1 

    logging.info("Writing to {}".format(out_fn))

    header = ["year", "num of papers"]

    records = sorted(dict(paper_by_year).iteritems())


    with open(out_fn, 'w') as fout:
        fout.write(','.join(header) + "\n")
        for (year, year_cnt) in records:
            fout.write("{},{}\n".format(year, year_cnt))



    logging.info("DONE")
