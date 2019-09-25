""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]
"""
# External imports
import logging
from pprint import pprint
from pprint import pformat
from docopt import docopt
import glob
import os
from operator import itemgetter
import csv
import pdb

# Local imports

#=-----

GENDER_PROBS = {
    "male": [1, 0],
    "female": [0, 1],
    "unknown": [0.5, 0.5]
}

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

    names = {}
    total_count = 0
    for gender in ["male", "female", "unknown"]:
        gender_probs = GENDER_PROBS[gender]
        cur_fn = os.path.join(inp_fn, f"{gender}.csv")
        logging.info(f"Parsing {cur_fn}")
        for line in open(cur_fn, encoding = "utf8"):
            line = line.replace(",,", ",") # Fix a weird inconsistency 
            name, count = line.strip().split(",")
            count = int(count)
            total_count += count
            if name not in names:
                names[name] =  [count] + gender_probs
            else:
                names[name][0] += count

    names = [[name] + values for name, values in names.items()]

    sorted_names = sorted(names, key = itemgetter(1), reverse = True)

    acc = []
    total_prob = 0
    for name, count, male_prob, female_prob in sorted_names:
        total_prob += count / total_count
        acc.append(round(total_prob, 4))

    with open(out_fn, "w", encoding = "utf8") as fout:
        # Header
        fout.write(",".join(["First name", "Count", "genderize_m", "genderize_f", "acc"]) + "\n")
        for (first_name, count, genderize_m, genderize_f), acc in zip(sorted_names, acc):
            fout.write(",".join(map(str, (first_name, count, genderize_m, genderize_f, acc))) + "\n")

    logging.info("DONE")
