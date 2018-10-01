""" Usage:
    <file-name> --in=IN_FILE --from=YEAR --out=OUT_FILE [--debug]
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
import networkx as nx

# Local imports

#=-----

def short_venue_name(year, venue_name):
    """
    Get shortened venue name.
    """
    return "{}_{}".format(year,
                          "".join([w[: 2].capitalize() for w in venue_name.split(" ")]))

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    start_year = int(args["--from"])
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    # eval
    venues = map(eval,
                 ["[{}]".format(line.strip()) for line in open(inp_fn)])

    venues_per_year = defaultdict(lambda: defaultdict(lambda: 0))

    for cur_venues in tqdm(venues):
        year = cur_venues[0]
        if year >=  start_year:
            for entry in cur_venues[1: ]:
                venue, cnt = entry
                venues_per_year[venue][year] = cnt

    sorted_venues = sorted(venues_per_year.items(),
                           key = lambda(k, v): sum(v.itervalues()),
                           reverse = True)
    years = range(start_year, 2018)
    with open(out_fn, "w") as fout:
        fout.write(",".join([""] + map(str, years)) + "\n")
        for venue, venue_dict in sorted_venues:
            fout.write(",".join([venue] + [str(venue_dict[year])
                                           for year in years]) + "\n")
    logging.info("DONE")
