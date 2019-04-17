""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--total=TOTAL] [--debug]

Answer:

1. Is the number (proportion) of female authors increasing?
2. Is the number (proportion) of female first authors increasing?
6. Bechedel
"""
# import sys
# # sys.setdefaultencoding() does not exist, here!
# reload(sys)  # Reload does the trick!
# sys.setdefaultencoding('UTF8')

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
    total = int(args["--total"]) if args["--total"] is not None \
            else None

    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    gender_dict = defaultdict(lambda: defaultdict(lambda: 0))
    gender_by_year = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

    for paper in tqdm(lazy_paper_reader(inp_fn), total = total):
        for author in paper["authors"]:
            first_name = author["first_name"].strip()
            if first_name:
                gender_dict[author["gender"]][first_name] += 1
                gender_by_year[author["gender"]][paper["year"]][first_name] += 1

    for gender in gender_dict:
        cur_fn = os.path.join(out_fn, "{}.csv".format(gender))
        logging.info("Writing to {}".format(cur_fn))
        with open(cur_fn, 'w') as fout:
            fout.write('\n'.join(["{},{}".format(name, count)
                                  for (name, count)
                                  in sorted(gender_dict[gender].items(),
                                            key = itemgetter(1),
                                            reverse = True)]))

    logging.info("DONE")
