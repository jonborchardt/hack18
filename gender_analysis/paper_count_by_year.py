""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

Answer:

1. Is the number (proportion) of female authors increasing?
2. Is the number (proportion) of female first authors increasing?
6. Bechedel
"""
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
import os
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
    authorship_by_year = defaultdict(lambda: 0)


    for paper in tqdm(lazy_paper_reader(inp_fn)):
        cur_authors = paper["authors"]
        paper_year = paper["year"]

        # add first and last author stats -- only for non-alphabetical
        if cur_authors:
            paper_by_year[paper_year] += 1
            authorship_by_year[paper_year] += len(cur_authors)

    logging.info("Writing to {}".format(out_fn))

    header = ["year", "num of papers", "authorship count"]

    records = sorted(dict(paper_by_year).items())

    with open(out_fn, 'w') as fout:
        fout.write(','.join(header) + "\n")
        for (year, year_paper_cnt) in records:
            fout.write("{},{},{}\n".format(year, year_paper_cnt, authorship_by_year[year]))

    logging.info("DONE")
