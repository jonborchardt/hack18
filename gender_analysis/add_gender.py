""" Usage:
    add_gender --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

Add a gender column to the an S2 input file (json lines), output written to a
new file.
"""
# Set default encoding to utf8
# import sys
# reload(sys) 
# sys.setdefaultencoding('UTF8')

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
#from legenderary.leGenderary import leGenderary
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
#gender = leGenderary(options)

def get_gender(full_name):
    """
    Return the gender of this name.
    """
    return gender.determineGender(full_name)


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
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)


    # Load input file
    logging.info("Adding gender...")
    authors_count = 0
    empty_cnt = 0
    with open(out_fn, 'w') as fout:
        for paper in tqdm(lazy_paper_reader(inp_fn)):
            author_ls = []
            for author in paper["authors"]:
                cur_author = {"name": author}
                authors_count += 1
                first_name = gender.determineFirstName(author.split())
                if first_name.strip():
                    cur_author['first_name'] = first_name
                    cur_author['gender'] = gender.determineGender(author)
                    author_ls.append(cur_author)
                else:
                    empty_cnt += 1

            paper["authors"] = author_ls
            fout.write('{}\n'.format(json.dumps(paper)))


    logging.info("Removed {} empty authors".format(empty_cnt))
    logging.info("Added gender to {} authors in {}".format(authors_count, out_fn))

    logging.info("DONE")
