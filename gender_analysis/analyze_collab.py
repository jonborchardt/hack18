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
                         ["male_male",
                          "female_male",
                          "male_female"
                          "female_female"])

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


    collab_by_year = defaultdict(lambda: defaultdict(lambda: 0))


    for paper in tqdm(lazy_paper_reader(inp_fn)):
        cur_year_record = collab_by_year[paper["year"]]
        cur_authors = paper["authors"]

        # all authors stats
        if len(cur_authors) > 1:
            for first_ind, cur_first_author in enumerate(cur_authors[: -1]):
                gender1 = cur_first_author["gender"]
                for cur_second_author in cur_authors[first_ind + 1:]:
                    gender2 = cur_second_author["gender"]
                cur_year_record["{}_{}".format(gender1, gender2)] += 1

    logging.info("Writing to {}".format(out_fn))

    header = ["year", "male-male", "female-male", "female-female"]
    with open(out_fn, 'w') as fout:
        fout.write("{}\n{}".format(','.join(header),
                                   "\n".join([','.join(map(str,
                                                           [year,
                                                            year_record["male_male"],
                                                            year_record["female_male"] + year_record["male_female"],
                                                            year_record["female_female"]]))
                                              for (year, year_record)
                                              in sorted(dict(collab_by_year).iteritems())])))



    logging.info("DONE")
