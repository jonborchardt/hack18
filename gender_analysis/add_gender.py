""" Usage:
    add_gender --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

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
from legenderary.leGenderary import leGenderary
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
    logging.info("Reading {}".format(inp_fn))
    paper_jsons = [json.loads(line.strip())
                   for line
                   in open(inp_fn)]

    logging.info("Read {} paper records".format(len(paper_jsons)))

    logging.info("Adding gender...")
    authors_count = 0
    for paper in tqdm(paper_jsons):
        for author in paper["authors"]:
            authors_count += 1
            full_name = author['name']
            first_name = gender.determineFirstName(full_name.split())
            author['first_name'] = first_name
            author['gender'] = gender.determineGender(full_name)
            #TODO: gender.determineGender is supposed to be better, but throws a decoding error?


    logging.info("Added gender to {} authors".format(authors_count))

    # Write to file
    logging.info("Writing output to {}".format(out_fn))
    with open(out_fn, 'w') as fout:
        fout.write('\n'.join([json.dumps(paper)
                              for paper in paper_jsons]))
    logging.info("DONE")
