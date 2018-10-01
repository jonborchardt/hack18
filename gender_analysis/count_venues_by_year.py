""" Usage:
    <file-name> --in=INPUT_FILE --top=N_VENUES --out=OUTPUT_FILE [--debug]

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
    num_of_venues = int(args["--top"])
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    venue_dict = defaultdict(lambda: defaultdict(lambda: 0))

    for paper in tqdm(lazy_paper_reader(inp_fn)):
        venue_dict[paper["year"]][paper["venue"]] += 1

    with open(out_fn, "w") as fout:
        for year, venues in venue_dict.items():
            sorted_venues = sorted(venues.items(),
                                   key = lambda(v, cnt): cnt,
                                   reverse = True)
            top_venues = sorted_venues[: num_of_venues]
            fout.write("{}::{}\n".format(year,
                                         ",".join(map(str, top_venues))))

    logging.info("DONE")
