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
from tqdm import tqdm

# Local imports
from add_gender import lazy_paper_reader
#=-----

from collections import namedtuple



year_record = namedtuple("YearRecord",
                         ["in_citation_by_gender"])



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


    in_citation_by_year = defaultdict(lambda: defaultdict(lambda: 0))


    for paper in tqdm(lazy_paper_reader(inp_fn)):
        cur_year_record = in_citation_by_year[paper["year"]]

        # all authors stats
        for cur_author in paper["authors"]:
            cur_year_record[cur_author["gender"]] += len(paper["inCitations"])

    logging.info("Writing to {}".format(out_fn))

    header = ["year", "male-in-citations", "female-in-citations", "unknown-in-citations"]
    with open(out_fn, 'w') as fout:
        fout.write("{}\n{}".format(','.join(header),
                                   "\n".join([','.join(map(str,
                                                           [year,
                                                            year_record["male"],
                                                            year_record["female"],
                                                            year_record["unknown"]]))
                                              for (year, year_record)
                                              in sorted(dict(in_citation_by_year).iteritems())])))



    logging.info("DONE")
