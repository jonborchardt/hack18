""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]
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
from genderize import Genderize
from tqdm import tqdm

# Local imports

#=-----

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

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


    # Extract first names
    first_names = ["".join(line.strip().split(",")[: -1])
                   for line in open(inp_fn)]

    g = Genderize()
    cnt = 0
    with open(out_fn, 'w') as fout:
        for name_chunks in tqdm(chunks(first_names, 10), total = len(first_names) / 10):
            cnt += len(name_chunks)
            data = g.get(name_chunks)
            fout.write('\n'.join(["{},{}".format(name, ret['gender'])
                                  for name, ret in zip(name_chunks, data)]) + '\n')

    logging.debug("Wrote {} names".format(cnt))
    logging.info("DONE")
