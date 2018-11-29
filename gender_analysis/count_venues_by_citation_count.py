""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--n=NUM_OF_PAPERS] [--debug]

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

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    debug = args["--debug"]
    num_of_papers = int(args["--n"]) if args["--n"] is not None \
                    else None
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    venue_dict = defaultdict(lambda: 0)

    for paper in tqdm(lazy_paper_reader(inp_fn), total = num_of_papers):
        venue_dict[paper["venue"]] += len(paper["inCitations"])

    with open(out_fn, "w") as fout:
        for venue, cnt in sorted(venue_dict.items(), key = lambda (v, cnt): cnt, reverse = True):
            fout.write("{},{}\n".format(venue, cnt))

    logging.info("DONE")
