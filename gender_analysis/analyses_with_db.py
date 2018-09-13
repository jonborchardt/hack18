""" Usage:
    add_gender --json=JSON_FILE --db=DB_FILE --out=OUTPUT_FILE [--debug]

Add a gender column to the an S2 input file (json lines), output written to a
new *sqlite* file.
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
from collections import namedtuple
import json
import sqlite3
import os

# Local imports
from add_gender import lazy_paper_reader
from sqlite_manager import Sqlite_Database
#=-----


class Out_Analysis:
    """
    Calculate out citation analysis per year
    """
    def __init__(self, db, base_dir):
        """
        Initialize analysis.
        """
        self.db = db
        self.data = defaultdict(lambda: defaultdict(lambda: 0))
        self.self_citations = defaultdict(lambda: defaultdict(lambda: 0))
        self.base_dir = base_dir
        self.out_fn = os.path.join(base_dir, "out_citation_analysis.csv")
        self.out_fn_self_citations = os.path.join(base_dir, "self_citation_analysis.csv")
        self.header = ["year", "male-out-citations", "female-out-citations", "unknown-out-citations"]
        self.self_cite_header = ["year", "male-self-cite", "female-self-cite", "unknown-self-cite"]

    def get_description(self):
        """
        Return a string describing this analysis.
        """
        return "out citation analysis"

    def add_paper(self, paper):
        """
        Add a single paper to the analysis
        """
        year = paper["year"]
        cur_authors = [author["name"]
                       for author
                       in paper["authors"]]
        cur_year_record = self.data[year]
        cur_year_self_citations_record = self.self_citations[year]

        for out_citation in paper["outCitations"]:
            for cited_gender, cited_author in zip(*db.get_paper_data(out_citation)):
                # Count gender out citations
                cur_year_record[cited_gender] += 1

                # Analyze self citations
                if cited_author in cur_authors:
                    # These author cited themselves
                    cur_year_self_citations_record[cited_gender] += 1

    def output_stats(self):
        for cur_out_fn, header, data in [(self.out_fn, self.header, self.data),
                                         (self.out_fn_self_citations, self.self_cite_header, self.self_citations)]:
            logging.info("Writing out citation analysis to {}".format(cur_out_fn))
            with open(cur_out_fn, 'w') as fout:
                fout.write("{}\n{}".format(','.join(header),
                                           "\n".join([','.join(map(str,
                                                                   [year,
                                                                    year_record["male"],
                                                                    year_record["female"],
                                                                    year_record["unknown"]]))
                                                      for (year, year_record)
                                                      in sorted(dict(data).iteritems())])))


if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    db_fn = args["--db"]
    json_fn = args["--json"]
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    # Run analyses
    with Sqlite_Database(db_fn) as db:
        analyses = [analysis(db, out_fn)
                    for analysis
                    in [Out_Analysis]]

        paper_cnt = 0

        for paper in tqdm(lazy_paper_reader(json_fn)):
            paper_cnt += 1
            for analysis in analyses:
                analysis.add_paper(paper)

    for analysis in analyses:
        analysis.output_stats()

    logging.info("Wrote analyses of {} papers to {}".format(paper_cnt,
                                                            out_fn))
    logging.info("DONE")
