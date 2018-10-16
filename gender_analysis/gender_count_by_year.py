""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

Answer:

1. Is the number (proportion) of female authors increasing?
2. Is the number (proportion) of female first authors increasing?
6. Bechedel
"""
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
import json
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter

# Local imports
from add_gender import lazy_paper_reader
#=-----

from collections import namedtuple

year_record = namedtuple("YearRecord",
                         ["total",
                          "first_author",
                          "last_author"])

def bracket(y, bracket_every):
    """
    Bracket data -- y axes.
    """
    return  [sum(y[ind : ind + bracket_every])
             for ind in range(0, len(y), bracket_every)]

def plot_stacked_bars(xticks, bars, width, interpolate, bracket_every, smooth, scale, colors, plt_params):
    """
    Plot stacked bars to file.
    https://matplotlib.org/examples/pylab_examples/bar_stacked.html
    """
    # Scale if needed
    if bracket_every != -1:
        xticks = xticks[:: bracket_every]
        for bar_index, bar in enumerate(bars):
            bars[bar_index] = bracket(bar, bracket_every)

    if interpolate:
        from scipy.interpolate import interp1d
        xticks_new = range(xticks[0], xticks[-1])
        for bar_index, bar in enumerate(bars):
            f = interp1d(xticks, bar, kind = "cubic")
            bars[bar_index] = f(xticks_new)
        xticks = xticks_new

    if smooth:
        bars = [savgol_filter(bar, 5, 3)
                for bar in bars]

    if scale:
        totals = np.array(map(sum, zip(*bars)), dtype = float)
        assert all(totals)
        for bar_index, bar in enumerate(bars):
            bars[bar_index] = np.array(bar, dtype = float) / totals

    # Plot
    legend = plt_params["legend"]
    ps = []
    plt.ticklabel_format(style = "plain")

    bars = [[val * plt_params["y_factor"] for val in bar]
            for bar in bars]

    for bar_index, (bar, color) in enumerate(zip(bars, colors)):
        bottoms = [sum(prev_bars)
                   for prev_bars in zip(*bars[: bar_index])]
        if bottoms:
            ps.append(plt.bar(xticks, bar, width, color = color,
                              bottom = bottoms,
                              label = legend[bar_index]))
        else:
            ps.append(plt.bar(xticks, bar, width, color = color,
                              label = legend[bar_index]))

    # Metadata
    plt.title(plt_params["title"])
    plt.ylabel(plt_params["ylabel"])
    plt.xlabel(plt_params["xlabel"])
    plt.xticks(xticks[::plt_params["xtick_spacing"]])

def plot_authorship(year_records, dirname):
    """
    Plot a stacked bar chart of authorship counts
    by gender.
    """
    # Collect data
    years = map(itemgetter(0), year_records)
    male_authorship = [year_record.total["total-male"]
                       for _, year_record in year_records]
    female_authorship = [year_record.total["total-female"]
                       for _, year_record in year_records]
    unknown_authorship = [year_record.total["total-unknown"]
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
                                    "ylabel": "# Papers [Millions]",
                                    "xlabel": "Year",
                                    "legend": ("Male", "Female", "Unknown"),
                                    "xtick_spacing": 10,
                                    "y_factor": float(1) / pow(10, 6)})
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
                                    "ylabel": "% Papers",
                                    "xlabel": "Year",
                                    "legend": ("Male", "Female"),
                                    "xtick_spacing": 10,
                                    "y_factor": float(100)})
    plt.axhline(y = 50)
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

    gender_by_year = defaultdict(lambda: year_record(defaultdict(lambda: 0),
                                                     defaultdict(lambda: 0),
                                                     defaultdict(lambda: 0)))


    for paper in tqdm(lazy_paper_reader(inp_fn)):
        cur_year_record = gender_by_year[paper["year"]]
        cur_authors = paper["authors"]

        # add first and last author stats
        if cur_authors:
            if len(cur_authors) > 1:
                # Avoid counting a single author as "junior"
                cur_year_record.first_author[cur_authors[0]["gender"]] += 1
            cur_year_record.last_author[cur_authors[-1]["gender"]] += 1

        # all authors stats
        for cur_author in cur_authors:
            cur_year_record.total[cur_author["gender"]] += 1

    logging.info("Writing to {}".format(out_fn))

    header = ["year", \
              "first-author-male", "first-author-female", "first-author-unkonwn",\
              "last-author-male", "last-author-female", "last-author-unkonwn",\
              "total-male", "total-female", "total-unknown"]

    records = sorted(dict(gender_by_year).iteritems())
    plot_authorship(records, "./")
    with open(out_fn, 'w') as fout:
        fout.write("{}\n{}".format(','.join(header),
                                   "\n".join([','.join(map(str,
                                                           [year,
                                                            year_record.first_author["male"],
                                                            year_record.first_author["female"],
                                                            year_record.first_author["unknown"],
                                                            year_record.last_author["male"],
                                                            year_record.last_author["female"],
                                                            year_record.last_author["unknown"],
                                                            year_record.total["male"],
                                                            year_record.total["female"],
                                                            year_record.total["unknown"]]))
                                              for (year, year_record)
                                              in records])))



    logging.info("DONE")
