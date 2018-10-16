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

    out_citations_dict = defaultdict(lambda: 0)
    paper_cnt = defaultdict(lambda: 0)

    for paper in tqdm(lazy_paper_reader(inp_fn)):
        citations_cnt = len(paper["outCitations"])
        cur_year = paper["year"]
        if citations_cnt:
            out_citations_dict[cur_year] += len(paper["outCitations"])
            paper_cnt[cur_year] +=1 


    with open(out_fn, 'w') as fout:
        fout.write(",".join(["year",
                             "#out citations"]) + "\n")
        fout.write("\n".join(["{},{}".format(year, float(cnt)/paper_cnt[year])
                              for year, cnt in out_citations_dict.iteritems()]))

    logging.info("DONE")
