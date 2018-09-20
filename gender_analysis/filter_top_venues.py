""" Usage:
    <file-name> --in=INPUT_FILE --venues=VENUES_FILE --top=TOP_N --out=OUTPUT_FILE  [--debug]

* Filter only articles published at one of the top n venues.
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

# Local imports
from add_gender import lazy_paper_reader
#=-----

from collections import namedtuple


def normalize_source(source):
    """
    Normalize a paper source.
    """
    return source.lower().rstrip().lstrip()


if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    debug = args["--debug"]
    venues_fn = args["--venues"]
    top_k = int(args["--top"])
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    top_venues = dict([(k, None) for k in
                       [''.join(line.strip().split(',')[: -1])
                        for line in open(venues_fn)][: top_k]])

    cnt = 0
    with open(out_fn, 'w') as fout:
        for paper in tqdm(lazy_paper_reader(inp_fn)):
            if paper["venue"] in top_venues:
                cnt +=1
                fout.write("{}\n".format(json.dumps(paper)))

    logging.info("Wrote {} papers to {}".format(cnt, out_fn))
    logging.info("DONE")
