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
from legenderary.leGenderary import leGenderary
#=-----

options = { 'male'          : 'male',
            'female'        : 'female',
            'androgynous'   : 'unknown',
            'unknown'       : 'unknown',
            'maleConfirm'   : 'male',
            'femaleConfirm' : 'female',
            'dict1'         : 'legenderary/dict1.txt',
            'dict2'         : 'legenderary/dict2.txt',
            'customDict'    : 'legenderary/custom.txt',
            'bingAPIKey'    : 'ABC123478ZML'
          }

# Init leGenderary
gender = leGenderary(options)

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

    cnt = 0

    with open(out_fn, 'w') as fout:
        for paper in tqdm(lazy_paper_reader(inp_fn)):
            non_empty_auth = [author
                              for author in paper["authors"]
                              if gender.determineFirstName(author.split())]
            cnt += len(paper["authors"]) - len(non_empty_auth)
            paper["authors"] = non_empty_auth
            fout.write("{}\n".format(json.dumps(paper)))

    logging.info("Removed {} nameless authors".format(cnt))
    logging.info("DONE")
