""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--filter] [--debug]

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

# Local imports
from add_gender import lazy_paper_reader
#=-----

from collections import namedtuple



year_record = namedtuple("YearRecord",
                         ["total",
                          "first_author",
                          "last_author"])

def count_last_female(papers):
    """
    Number of female last authors in papers.
    """
    return len([paper for paper in papers
                if paper["authors"][-1]["gender"] == "female"])


def get_papers_by_year(papers, year):
    """
    Return papers published in a given year
    """
    return [paper for paper in papers
            if paper["year"] == year]


def is_problematic_venue(venue_papers):
    """
    Assess if this is a problematic venue.
    """
    old = get_papers_by_year(venue_papers, 2001)
    new = get_papers_by_year(venue_papers, 2002)
    assert len(old) + len(new) == len(venue_papers)
    return count_last_female(old) - count_last_female(new)

def get_last_name(author):
    """
    Get an author's last name.
    """
    return author["name"].split(" ")[-1]

def is_alphabetical(paper):
    """
    Check if a paper's authors are listed by alphabetical
    order.
    """
    last_names = [get_last_name(author).lower()
                  for author in paper["authors"]]
    return sorted(last_names) == last_names

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    debug = args["--debug"]
    filter_flag = args["--filter"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    logging.info("Reading papers from {}".format(inp_fn))
    if filter_flag:
        papers = []
        for paper in tqdm(lazy_paper_reader(inp_fn), total = 12491238):
            if (any([author["gender"] != "unknown"
                     for author in paper["authors"]])) and \
                         ((paper["year"] == 2001) or (paper["year"] == 2002)):
                papers.append(paper)
    else:
        papers = list(lazy_paper_reader(inp_fn))
        papers_by_venues = defaultdict(list)
        for paper in papers:
            papers_by_venues[paper["venue"]].append(paper)

    logging.info("Checking alphabetical...")
    old_alph = filter(is_alphabetical,
                      get_papers_by_year(papers, 2001))

    new_alph = filter(is_alphabetical,
                      get_papers_by_year(papers, 2002))

    logging.info("old alph: {}\n new alph: {}".format(len(old_alph),
                                                      len(new_alph)))
    logging.info("DONE")
