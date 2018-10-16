""" Usage:
    <file-name> --in=IN_FILE --out=OUT_FILE --window=WINDOW --poly=POLY [--debug]
"""
# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
from tqdm import tqdm
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

# Local imports

#=-----

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    poly = int(args["--poly"])
    window = int(args["--window"])
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    y = []
    for line in open(inp_fn):
        try:
            y.append(float(line.strip()))
        except:
            pass

    logging.info("Read {} float values from {}".format(len(y), inp_fn))

    y_smoothed = savgol_filter(y, window, poly)
    x = range(1970, 2018)
    plt.plot(x, y)
    plt.plot(x, y_smoothed, color="red")
    plt.show()

    logging.info("Writing output to {}".format(out_fn))
    with open(out_fn, "w") as fout:
        fout.write("\n".join(map(str, y_smoothed)))

    logging.info("DONE")
