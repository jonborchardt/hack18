""" Usage:
    <file-name> --auth=AUTHORSHIP_COUNT --cites=CITATION_FILE --colab=COLLAB_FILE --out=OUT_FOLDER [--debug]
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
from gender_count_by_year import plot_stacked_bars
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import numpy as np
from gender_count_by_year import bracket


# Local imports
from gender_count_by_year import year_record
from gender_count_by_year import plot_authorship
#=-----

# Plot authorship
# Plot citation
# Plot collaboration

EXPECTED_COLOR = "green"

def try_to_int(val):
    """
    Try to return an int out of val.
    """
    try:
        return int(val)
    except:
        return val

def read_file(inp_fn):
    """
    Parse an input file.
    """
    lines = [line.strip().split(",")
             for line in open(inp_fn)
             if not (line.startswith("#"))]
    header = lines[0][1:]
    return [(int(line[0]), year_record(dict(zip(header, map(try_to_int,
                                                            line[1:]))),
                                       None, None))
            for line in lines[1:]]

def plot_collaboration(year_records, dirname):
    """
    Plot a stacked bar chart of collaborations by
    gender.
    """
    # Calculate expected lines
    total_male = np.array(bracket([float(record.total["total-male"])
                                   for _, record in year_records],
                                  5))
    total_female = np.array(bracket([float(record.total["total-female"])
                                     for _, record in year_records],
                                    5))
    male_prob = total_male / (total_female + total_male)
    female_prob = total_female / (total_female + total_male)
    expected_male_male = pow(male_prob, 2) * 100


    # Draw lines
    years = map(itemgetter(0), year_records)
    male_male = [year_record.total["male-male"]
                 for _, year_record in year_records]
    female_male = [year_record.total["female-male"]
                   for _, year_record in year_records]
    female_female = [year_record.total["female-female"]
                     for _, year_record in year_records]

    # Plot counts
    collab_proportion_filename = os.path.join(dirname, "collab_proportions.png")
    logging.info("Writing to {}".format(collab_proportion_filename))
    plot_stacked_bars(years,
                      [male_male, female_male, female_female],
                      width = 0.9,
                      interpolate = True,
                      bracket_every = 5,
                      smooth = True,
                      scale = True,
                      colors=["blue", "orange", "red"],
                      plt_params = {"title": "Collaboration proportions",
                                    "ylabel": "% Collaboration",
                                    "xlabel": "Year",
                                    "legend": ("male-male", "female-male", "female-female"),
                                    "xtick_spacing": 10,
                                    "y_factor": 100})
    # Add expected lines
    plt.plot(years[::5], expected_male_male, "--", linewidth = 2, color="black")
    plt.legend()
    plt.savefig(collab_proportion_filename, bbox_inches = "tight")
    plt.clf()



def plot_citation(year_records, dirname):
    """
    Plot a stacked bar chart of citation counts
    by gender.
    """
    # Calculate expected line
    total_male = np.array(bracket([float(record.total["total-male"])
                                   for _, record in year_records],
                                  5))
    total_female = np.array(bracket([float(record.total["total-female"])
                                     for _, record in year_records],
                                    5))

    expected = (total_male / (total_male + total_female)) * 100
    expected = savgol_filter(expected, 5, 3)

    # Collect data
    years = map(itemgetter(0), year_records)
    male_cites = [year_record.total["male-out-citations"]
                  for _, year_record in year_records]
    female_cites = [year_record.total["female-out-citations"]
                    for _, year_record in year_records]
    unknown_cites = [year_record.total["unknown-out-citations"]
                     for _, year_record in year_records]
    female_to_female = [year_record.total["female->female"]
                        for _, year_record in year_records]
    female_to_male = [year_record.total["female->male"]
                      for _, year_record in year_records]
    male_to_male = [year_record.total["male->male"]
                        for _, year_record in year_records]
    male_to_female = [year_record.total["male->female"]
                      for _, year_record in year_records]


    # Plot counts
    citation_count_filename = os.path.join(dirname, "citation_counts.png")
    logging.info("Writing to {}".format(citation_count_filename))
    plot_stacked_bars(years,
                      [male_cites, female_cites, unknown_cites],
                      width = 0.9,
                      interpolate = True,
                      bracket_every = 3,
                      smooth = True,
                      scale = False,
                      colors=["blue", "orange", "red"],
                      plt_params = {"title": "Citation counts",
                                    "ylabel": "# Papers [Millions]",
                                    "xlabel": "Year",
                                    "legend": ("Male", "Female", "Unknown"),
                                    "xtick_spacing": 10,
                                    "y_factor": float(1) / pow(10, 6)})
    plt.legend()
    plt.savefig(citation_count_filename, bbox_inches = "tight")
    plt.clf()


    # Plot proportions
    author_proportion_filename = os.path.join(dirname, "citation_proportions.png")
    logging.info("Writing to {}".format(author_proportion_filename))

    plot_stacked_bars(years,
                      [male_cites, female_cites],
                      width = 1,
                      interpolate = True,
                      bracket_every = 5,
                      smooth = True,
                      scale = True,
                      colors=["blue", "orange"],
                      plt_params = {"title": "Citation proportions",
                                    "ylabel": "% Papers",
                                    "xlabel": "Year",
                                    "legend": ("Male", "Female"),
                                    "xtick_spacing": 10,
                                    "y_factor": float(100)})

    plt.axhline(y = 50)
    plt.plot(years[::5], expected, "--", linewidth = 3, color = EXPECTED_COLOR,
             label = "expected")
    plt.legend()

    plt.legend()
    plt.savefig(author_proportion_filename, bbox_inches = "tight")
    plt.clf()

    # Plot male citation patterns
    male_proportion_filename = os.path.join(dirname, "male_cite_pattern.png")
    logging.info("Writing to {}".format(male_proportion_filename))

    plot_stacked_bars(years,
                      [male_to_male, male_to_female],
                      width = 1,
                      interpolate = True,
                      bracket_every = 5,
                      smooth = True,
                      scale = True,
                      colors=["blue", "orange"],
                      plt_params = {"title": "Male citation pattern",
                                    "ylabel": "% Male Citation",
                                    "xlabel": "ear",
                                    "legend": ("->Males", "->Female", "expected"),
                                    "xtick_spacing": 10,
                                    "y_factor": float(100)})
    plt.axhline(y = 50)

    plt.plot(years[::5], expected, "--", linewidth = 3, color = EXPECTED_COLOR,
             label = "expected")
    plt.legend()
    plt.legend()
    plt.savefig(male_proportion_filename, bbox_inches = "tight")
    plt.clf()

    # Plot female citation patterns
    female_proportion_filename = os.path.join(dirname, "female_cite_pattern.png")
    logging.info("Writing to {}".format(female_proportion_filename))

    plot_stacked_bars(years,
                      [female_to_male, female_to_female],
                      width = 1,
                      interpolate = True,
                      bracket_every = 5,
                      smooth = True,
                      scale = True,
                      colors=["blue", "orange"],
                      plt_params = {"title": "Female citation pattern",
                                    "ylabel": "% Female citation",
                                    "xlabel": "Year",
                                    "legend": ("->Male", "->Female"),
                                    "xtick_spacing": 10,
                                    "y_factor": float(100)})
    plt.axhline(y = 50)
    plt.plot(years[::5], expected, "--", linewidth = 3, color = EXPECTED_COLOR,
             label = "expected")
    plt.legend()
    plt.savefig(female_proportion_filename, bbox_inches = "tight")
    plt.clf()

def merge_year_records(*records):
    """
    Return a merged year record.
    """
    ret = [x for x in records[0]]

    for record in records[1:]:
        for record_ind, (year, record) in enumerate(record):
            ref_year, ref_record = ret[record_ind]
            assert year == ref_year
            ref_record.total.update(record.total)
    return ret

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    auth_fn = args["--auth"]
    cites_fn = args["--cites"]
    collab_fn = args["--colab"]
    out_dir = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    year_records = merge_year_records(read_file(auth_fn),
                                      read_file(cites_fn),
                                      read_file(collab_fn))

    plot_authorship(year_records, out_dir)
    plot_citation(year_records, out_dir)
    plot_collaboration(year_records, out_dir)

    logging.info("DONE")
