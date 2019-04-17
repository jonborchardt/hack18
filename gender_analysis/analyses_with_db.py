""" Usage:
    add_gender --json=JSON_FILE --db=DB_FILE --gender=GENDER_FN --out=OUTPUT_FILE [--n=NUM_OF_PAPERS] [--debug]

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
from collections import namedtuple
import json
import sqlite3
import os

# Local imports
from add_gender import lazy_paper_reader
from sqlite_manager import Sqlite_Database
from util import get_gender_prob, load_name_probs
from gender_count_by_year import add_author
from analyze_collab import add_collab
#=-----

class Out_Analysis:
    """
    Calculate out citation analysis per year
    """
    def __init__(self, db, gender_dict, base_dir):
        """
        Initialize analysis.
        """
        self.db = db
        self.gender_dict = gender_dict
        self.miss_cnt = 0
        self.data = defaultdict(lambda: defaultdict(lambda: 0))
        self.self_citations = defaultdict(lambda: defaultdict(lambda: 0))
        self.base_dir = base_dir
        self.out_fn = os.path.join(base_dir, "out_citation_analysis.csv")
        self.out_fn_self_citations = os.path.join(base_dir, "self_citation_analysis.csv")
        self.header = ["year", "male-out-citations", "female-out-citations", "unknown-out-citations",
                       "male->male", "male->female", "female->female", "female->male"]
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
        cur_author_names = [author["name"]
                            for author
                            in paper["authors"]]
        cur_year_record = self.data[year]
        cur_year_self_citations_record = self.self_citations[year]

        for out_citation in paper["outCitations"]:
            cited_paper = db.get_paper_data(out_citation)
            pdb.set_trace()
            if cited_paper is None:
                # cited paper is outside the corpus
                self.miss_cnt += 1
                continue
            for cited_author in cited_paper["authors"]:
                # Count gender out citations

                add_author(cur_year_record, self.gender_dict, cited_autor)
#                cur_year_record[cited_author["gender"]] += 1

                # Analyze self citations
                if cited_author["name"] in cur_author_names:
                    # These author cited themselves
                    add_author(cur_year_self_citations_record,
                               self.gender_dict, cited_author)
#                    cur_year_self_citations_record[cited_author["gender"]] += 1

                # Count interactions
                for citing_author in paper["authors"]:
                    add_collab(cur_year_record, self.gender_dict,
                               citing_author, cited_author)
                    # interaction = "{}_{}".format(citing_author["gender"],
                    #                               cited_author["gender"])
                    # cur_year_record[interaction] += 1

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
                                                                    year_record["unknown"],
                                                                    year_record["male_male"],
                                                                    year_record["male_female"],
                                                                    year_record["female_female"],
                                                                    year_record["female_male"],
                                                                   ]))
                                                      for (year, year_record)
                                                      in sorted(dict(data).items())])))


if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    db_fn = args["--db"]
    gender_fn = args["--gender"]
    json_fn = args["--json"]
    out_fn = args["--out"]
    num_of_papers = int(args["--n"]) if args["--n"] is not None \
                    else None

    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    gender_dict = load_name_probs(gender_fn)

    # Run analyses
    with Sqlite_Database(db_fn) as db:
        analyses = [analysis(db, gender_dict, out_fn)
                    for analysis
                    in [Out_Analysis]]

        paper_cnt = 0

        for paper in tqdm(lazy_paper_reader(json_fn), total = num_of_papers):
            paper_cnt += 1
            for analysis in analyses:
                analysis.add_paper(paper)

    for analysis in analyses:
        analysis.output_stats()

    logging.info("Wrote analyses of {} papers to {}".format(paper_cnt,
                                                            out_fn))
    logging.info("DONE")
