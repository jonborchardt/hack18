""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]
"""
# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
import pandas as pd

# Local imports
import add_gender
from legenderary.leGenderary import leGenderary
#=-----

def get_majority(annots):
    """
    Get the majority annotation and its count
    """
    maj = max(set(annots), key =  annots.count)
    return (maj, annots.count(maj))

def get_human_agreement(annots_fn):
    """
    Get tuples of (first_name, gender) agreed upon
    by all annotators.
    """
    lines = [line.split('\t')
             for line in open(annots_fn)][1:]
    ret = []
    disagree = []
    for data in lines:
        maj, cnt = get_majority([annot[0]
                                 for annot in data[2:]])
        if cnt >= 3:
            ret.append((data[0],
                        maj))
        else:
            disagree.append(data[0])
    return ret, disagree, float(len(ret)) / len(lines)



options = { 'male'          : 'M',
            'female'        : 'F',
            'androgynous'   : '?',
            'unknown'       : '?',
            'maleConfirm'   : 'M',
            'femaleConfirm' : 'F',
            'dict1'         : 'legenderary/dict1.txt',
            'dict2'         : 'legenderary/dict2.txt',
            'customDict'    : 'legenderary/custom.txt',
            'bingAPIKey'    : 'ABC123478ZML'
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

    agree = get_human_agreement(inp_fn)
    logging.info(agree[2])
    gender_pred = leGenderary(options)

    correct = []
    false = []
    for (name, gender) in agree[0]:
        predicted = gender_pred.determineGender(name)
        if predicted == gender:
            correct.append((name,
                            gender))
        else:
            false.append((name,
                          predicted,
                          gender))


    acc = float(len(correct)) / len(agree[0])

    logging.info("acc = {}".format(acc))

    logging.info("DONE")
