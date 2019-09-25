""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]
"""
# External imports
import logging
import os
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from operator import itemgetter

# Local imports

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

    lines = [line.strip().split(",") for line in open(inp_fn, encoding = "utf8")][1 : 5000]
    weighted_names_male = {}
    weighted_names_female = {}
    prev_acc = 0

    for name, _, _, _, cur_acc, prob_m, prob_f in lines:
        cur_acc = float(cur_acc)
        prob_m = float(prob_m)
        prob_f = float(prob_f)
        percent = cur_acc - prev_acc
        prev_acc = cur_acc
        if abs(prob_m - prob_f) > 0.8:
            if prob_m > prob_f:
                weighted_names_male[name] = prob_m * percent

            else:
                weighted_names_female[name] = prob_f * percent

    weighted_names_male = sorted(weighted_names_male.items(),
                                 key = itemgetter(1), reverse = True)
    weighted_names_female = sorted(weighted_names_female.items(),
                                   key = itemgetter(1), reverse = True)

    female_fn = os.path.join(out_fn, "female.csv")
    male_fn = os.path.join(out_fn, "male.csv")

    for cur_dict, cur_fn in zip([weighted_names_male, weighted_names_female],
                                [male_fn, female_fn]):
        with open(cur_fn, "w", encoding = "utf8") as fout:
            logging.info(f"Writing to {cur_fn}")
            fout.write("name,correct?\n")
            fout.write("\n".join([f"{name}," for name, _ in cur_dict]))

    logging.info("DONE")
