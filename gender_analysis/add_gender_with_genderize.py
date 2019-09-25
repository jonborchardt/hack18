""" Usage:
    add_gender --in=INPUT_FILE --out=OUTPUT_FILE [--api=API_KEY] [--n=NUM_OF_PAPERS] [--debug]

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
from genderize import Genderize, GenderizeException
from operator import itemgetter
from tqdm import tqdm
import json

# Local imports
from legenderary.leGenderary import leGenderary
from genderize_name_list import sanitize
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

def get_gender(full_name):
    """
    Return the gender of this name.
    """
    return gender.determineGender(full_name)


def is_initial(first_name):
    """
    Simple heuristic to weed out some initials.
    """
    return (len(first_name) <= 5) and ("." in first_name)

def lazy_paper_reader(fn):
    """
    Read jsonl file lazyly
    """
    for line in open(fn):
        yield(json.loads(line.strip()))

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    api_key = args["--api"]
    num_of_papers = int(args["--n"]) if args["--n"] is not None \
                    else None

    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    name_cache = {}

    # Load input file
    logging.info("Adding gender...")
    authors_count = 0
    empty_cnt = 0

    g = Genderize(api_key = api_key) if api_key is not None \
        else Genderize()

    with open(out_fn, 'w') as fout:
        for paper in tqdm(lazy_paper_reader(inp_fn), total = num_of_papers):
            author_ls = []
            for author in paper["authors"]:
                authors_count += 1
                first_name = sanitize(author["first_name"])
                if first_name.strip():
                    if first_name in name_cache:
                        cur_gender = name_cache[first_name]
                    else:
                        cur_gender = g.get([first_name])[0]["gender"]
                        if not(cur_gender):
                            cur_gender = "unknown"
                        name_cache[first_name] = cur_gender

                    author['gender'] =cur_gender
                    author["is_initial"] = is_initial(first_name)
                    author_ls.append(author)
                else:
                    empty_cnt += 1

            paper["authors"] = author_ls
            fout.write('{}\n'.format(json.dumps(paper)))


    logging.info("Removed {} empty authors".format(empty_cnt))
    logging.info("Added gender to {} authors in {}".format(authors_count, out_fn))

    logging.info("DONE")
