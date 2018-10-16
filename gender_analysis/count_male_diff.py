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
import os
from tqdm import tqdm
from collections import namedtuple

# Local imports
from add_gender import lazy_paper_reader
#=-----

def get_last_name(author):
    """
    Get an author's last name.
    """
    return author["name"].split(" ")[-1]

def is_alphabetical(paper):
    """
    Check if a paper's authors are listed by alphabetical
    order.
    """
    last_names = [get_last_name(author).lower()
                  for author in paper["authors"]]
    return sorted(last_names) == last_names

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

    ab_by_year = defaultdict(lambda: 0)

    for paper in tqdm(lazy_paper_reader(inp_fn)):
        if paper["authors"]:
            ab_by_year[paper["year"]][is_alphabetical(paper)] += 1

    logging.info("Writing to {}".format(out_fn))
    with open(out_fn, 'w') as fout:
        fout.write(",".join(["year",
                             "ab",
                             "non-ab"]) + "\n")
        for year, values_dict in ab_by_year.iteritems():
            fout.write("{},{},{}\n".format(year,
                                           values_dict[True],
                                           values_dict[False]))

    logging.info("DONE")
