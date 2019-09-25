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
import html

# Local imports
from add_gender import lazy_paper_reader
#=-----

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    debug = args["--debug"]
    total = int(args["--total"]) if args["--total"] is not None \
            else None
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    gender_dict = defaultdict(lambda: defaultdict(lambda: 0))
    gender_by_year = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

    with open(out_fn, "w") as fout:
        for paper in tqdm(lazy_paper_reader(inp_fn), total = total):
            for author in paper["authors"]:
                first_name = author["first_name"]
                fixed_name = html.unescape(first_name).lower()
                if fixed_name != first_name:
                    logging.debug(f"Fixed {first_name} --> {fixed_name}")
                author["first_name"] = fixed_name
            fout.write('{}\n'.format(json.dumps(paper)))

    logging.info("DONE")
