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

# Local imports
from add_gender import lazy_paper_reader
#=-----

from collections import namedtuple





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


    gender_dict = defaultdict(lambda: defaultdict(lambda: 0))

    for paper in tqdm(lazy_paper_reader(inp_fn)):
        for author in paper["authors"]:
            gender_dict[author["gender"]][author["first_name"]] += 1

    for gender in gender_dict:
        with open(os.path.join(out_fn, "{}.csv".format(gender)), 'w') as fout:
            fout.write('\n'.join(["{},{}".format(name, count)
                                  for (name, count)
                                  in sorted(gender_dict[gender].iteritems(),
                                            key = lambda(key, value): value,
                                            reverse = True)]))

    logging.info("DONE")
