""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--api=API_KEY] [--debug]
"""
# Set default encoding to utf8
import sys
reload(sys) 
sys.setdefaultencoding('UTF8')


# External imports
import logging
from pprint import pprint
from pprint import pformat
from docopt import docopt
from genderize import Genderize, GenderizeException
from tqdm import tqdm
from unidecode import unidecode

# Local imports

#=-----

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def sanitize(first_name):
    """
    Clean a first name.
    """
    return unidecode(first_name.decode()).capitalize()

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    api_key = args["--api"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)


    # Extract first names
    first_names = [sanitize("".join(line.strip().split(",")[: -1]))
                   for line in open(inp_fn)]

    g = Genderize(api_key = api_key) if api_key is not None \
                            else Genderize()
    cnt = 0
    with open(out_fn, 'w') as fout:
        for name_chunks in tqdm(chunks(first_names, 10), total = len(first_names) / 10):
            try:
                data = g.get(name_chunks)
                fout.write('\n'.join(["{},{}".format(name, ret['gender'])
                                      for name, ret in zip(name_chunks, data)]) + '\n')
                cnt += len(name_chunks)

            except GenderizeException as e:
                logging.error("Couldn't genderize: {}".format(name_chunks))
                logging.error(e)

    logging.info("Wrote {} names".format(cnt))
    logging.info("DONE")
