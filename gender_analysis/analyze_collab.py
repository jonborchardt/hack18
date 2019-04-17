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

# Local imports
from add_gender import lazy_paper_reader
from util import load_name_probs, get_gender_prob
#=-----

from collections import namedtuple

year_record = namedtuple("YearRecord",
                         ["male_male",
                          "female_male",
                          "male_female"
                          "female_female"])

def add_collab(stats_dict, gender_dict, auth1, auth2):
    """
    Add a single collab to counts.
    """
    auth1_gender = get_gender_prob(gender_dict, auth1)
    auth2_gender = get_gender_prob(gender_dict, auth2)

    # Calculate probabilities of all combinations
    cur_sum = 0
    for gender1 in ["male", "female"]:
        for gender2 in ["male", "female"]:
            auth1_prob = auth1_gender[gender1]
            auth2_prob = auth2_gender[gender2]
            cur_prob = auth1_prob * auth2_prob
            cur_sum += cur_prob
            stats_dict[f"{gender1}_{gender2}"] += cur_prob

    # Sanity check
    if (round(cur_sum, 10) != 1):
        pdb.set_trace()
        raise AssertionError

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


    collab_by_year = defaultdict(lambda: defaultdict(lambda: 0))
    gender_dict = load_name_probs(gender_fn)


    for paper in tqdm(lazy_paper_reader(inp_fn)):
        cur_year_record = collab_by_year[paper["year"]]
        cur_authors = paper["authors"]

        # all authors stats
        if len(cur_authors) > 1:
            for first_ind, cur_first_author in enumerate(cur_authors[: -1]):
                for cur_second_author in cur_authors[first_ind + 1:]:
                    add_collab(cur_year_record, gender_dict,
                              cur_first_author, cur_second_author)

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
                                              in sorted(dict(collab_by_year).items())])))



    logging.info("DONE")
