""" Usage:
    <file-name> --in=IN_FILE  --out=OUT_FOLDER [--debug]
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

# Local imports
from gender_count_by_year import year_record
from gender_count_by_year import plot_authorship
#=-----

# Plot authorship
# Plot citation
# Plot collaboration


def read_file(inp_fn):
    """
    Parse an input file.
    """
    lines = [line.strip().split(",")
             for line in open(inp_fn)
             if not (line.startswith("#"))]
    return [(int(line[0]), year_record({"male": int(line[-3]),
                                   "female": int(line[-2]),
                                   "unknown": int(line[-1])},
                                  None, None))
            for line in lines[1:]]

def plot_authorship(year_records, dirname):
    """
    Plot a stacked bar chart of authorship counts
    by gender.
    """
    pdb.set_trace()
    # Collect data
    years = map(itemgetter(0), year_records)
    male_authorship = [year_record.total["male"]
                       for _, year_record in year_records]
    female_authorship = [year_record.total["female"]
                       for _, year_record in year_records]
    unknown_authorship = [year_record.total["unknown"]
                          for _, year_record in year_records]

    # Plot counts
    author_count_filename = os.path.join(dirname, "authorship_counts.png")
    logging.info("Writing to {}".format(author_count_filename))
    plot_stacked_bars(years,
                      [male_authorship, female_authorship, unknown_authorship],
                      width = 0.9,
                      interpolate = True,
                      bracket_every = 3,
                      smooth = True,
                      scale = False,
                      colors=["blue", "orange", "red"],
                      plt_params = {"title": "Authorship counts",
                                    "ylabel": "# Papers",
                                    "xlabel": "Year",
                                    "legend": ("Male", "Female", "Unknown"),
                                    "xtick_spacing": 10})
    plt.savefig(author_count_filename, bbox_inches = "tight")
    plt.clf()


    # Plot proportions
    author_proportion_filename = os.path.join(dirname, "authorship_proportions.png")
    logging.info("Writing to {}".format(author_proportion_filename))

    plot_stacked_bars(years,
                      [male_authorship, female_authorship],
                      width = 1,
                      interpolate = True,
                      bracket_every = 5,
                      smooth = True,
                      scale = True,
                      colors=["blue", "orange"],
                      plt_params = {"title": "Authorship proportions",
                                    "ylabel": "# Papers",
                                    "xlabel": "Year",
                                    "legend": ("Male", "Female"),
                                    "xtick_spacing": 10})
    plt.axhline(y = 0.5)
    plt.savefig(author_proportion_filename, bbox_inches = "tight")
    plt.clf()


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

    year_records = read_file(inp_fn)

    plot_authorship(year_records, out_fn)

    logging.info("DONE")
