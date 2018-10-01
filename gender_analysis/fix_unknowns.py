""" Usage:
    add_gender --in=INPUT_FILE --gender=GENDER_FILE --out=OUTPUT_FILE [--debug]

Add a gender column to the an S2 input file (json lines), output written to a
new file.
"""
# Set default encoding to utf8
import sys
reload(sys) 
sys.setdefaultencoding('UTF8')

# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
from tqdm import tqdm
import json

# Local imports
from genderize_name_list import sanitize
#=-----

def lazy_paper_reader(fn):
    """
    Read jsonl file lazyly.
    """
    for line in open(fn):
        yield(json.loads(line.strip()))

def load_genderized(fn):
    """
    Return a dict with genderized output.
    """
    ret = {}
    for line in open(fn):
        line = line.strip()
        data = line.split(",")
        first_name = "".join(data[: -1])
        gender = data[-1]
        if gender != "None":
            ret[first_name] = gender
    return ret

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


    # Load input file
    genderize_dict = load_genderized(gender_fn)

    logging.info("Adding gender...")
    cnt = 0
    with open(out_fn, 'w') as fout:
        for paper in tqdm(lazy_paper_reader(inp_fn)):
            author_ls = []
            for author in paper["authors"]:
                first_name = sanitize(author["first_name"])
                if (author["gender"] == "unknown") and (first_name in genderize_dict):
                    cnt += 1
                    author["gender"] = genderize_dict[first_name]

                author_ls.append(author)

            paper["authors"] = author_ls
            fout.write('{}\n'.format(json.dumps(paper)))

    logging.info("Added gender to {} authors in {}".format(cnt, out_fn))

    logging.info("DONE")
