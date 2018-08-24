""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

* Filter only articles published PubMed to the output file.

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
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    cnt = 0
    with open(out_fn, 'w') as fout:
        for paper in tqdm(lazy_paper_reader(inp_fn)):
            if "medline" in map(normalize_source,
                                paper["sources"]):
                cnt +=1
                fout.write("{}\n".format(json.dumps(paper)))


    logging.info("Wrote {} papers to {}".format(cnt, out_fn))
    logging.info("DONE")
