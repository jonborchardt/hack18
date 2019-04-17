""" Usage:
    <file-name> --in=INPUT_FILE --gender=GENDER_FN --out=OUTPUT_FILE [--debug]

Answer:

1. Is the number (proportion) of female authors increasing?
2. Is the number (proportion) of female first authors increasing?
6. Bechedel
"""
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
import os
from typing import Dict

# Local imports
from add_gender import lazy_paper_reader
from count_alphabetical import is_alphabetical
from util import load_name_probs, get_gender_prob
#=-----

from collections import namedtuple

year_record = namedtuple("YearRecord",
                         ["total",
                          "first_author",
                          "last_author",
                          "unique"])

def is_initial(first_name):
    """
    Simple heuristic to weed out some initials.
    """
    return (len(first_name) <= 10) and ("." in first_name)


def add_author(stats_dict: Dict, gender_dict: Dict, author: Dict):
    """
    Add a single author gender to stats
    """
    author_gender = get_gender_prob(gender_dict, author)
    stats_dict["male"] += author_gender["male"]
    stats_dict["female"] += author_gender["female"]

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    gender_fn = args["--gender"]
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    gender_dict = load_name_probs(gender_fn)

    gender_by_year = defaultdict(lambda: year_record(defaultdict(lambda: 0),
                                                     defaultdict(lambda: 0),
                                                     defaultdict(lambda: 0),
                                                     defaultdict(set)
                                                     ))


    for paper in tqdm(lazy_paper_reader(inp_fn)):
        cur_year_record = gender_by_year[paper["year"]]
        cur_authors = paper["authors"]

        # add first and last author stats -- only for non-alphabetical
        if cur_authors and (len(cur_authors) > 1):
            # Avoid counting a single author as "junior"
            if not(is_alphabetical(paper)):
                add_author(cur_year_record.first_author, gender_dict, cur_authors[0])
                add_author(cur_year_record.last_author, gender_dict, cur_authors[-1])

        # all authors stats
        for cur_author in cur_authors:
            cur_first_name = cur_author["first_name"]
            add_author(cur_year_record.total, gender_dict, cur_author)

            # Legacy:
            cur_year_record.unique[cur_author["gender"]].add(cur_first_name)
            if is_initial(cur_first_name):
                cur_year_record.total["initials"] += 1

    logging.info("Writing to {}".format(out_fn))

    header = ["year", \
              "first-author-male", "first-author-female", "first-author-unknown",\
              "last-author-male", "last-author-female", "last-author-unknown",\
              "total-male", "total-female", "total-unknown", "unique-male", "unique-female", "unique-unknown", "total_initials"]

    records = sorted(dict(gender_by_year).items())

    with open(out_fn, 'w') as fout:
        fout.write("{}\n{}".format(','.join(header),
                                   "\n".join([','.join(map(str,
                                                           [year,
                                                            year_record.first_author["male"],
                                                            year_record.first_author["female"],
                                                            year_record.first_author["unknown"],
                                                            year_record.last_author["male"],
                                                            year_record.last_author["female"],
                                                            year_record.last_author["unknown"],
                                                            year_record.total["male"],
                                                            year_record.total["female"],
                                                            year_record.total["unknown"],
                                                            len(year_record.unique["male"]),
                                                            len(year_record.unique["female"]),
                                                            len(year_record.unique["unknown"]),
                                                            year_record.total["initials"]]))
                                              for (year, year_record)
                                              in records])))



    logging.info("DONE")
