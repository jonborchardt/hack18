""" Usage:
    <file-name> --base=BASE_DB --papers=PAPER_IDS --out=OUTPUT_DB [--debug]
"""
# External imports
import logging
from pprint import pprint
from pprint import pformat
from docopt import docopt
from tqdm import tqdm
import pdb
# Local imports
from sqlite_manager import Sqlite_Database
#=-----

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    base_db_fn = args["--base"]
    papers_fn = args["--papers"]
    out_db_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    paper_ids = [int(line.strip()) for line in open(papers_fn)]

    with Sqlite_Database(base_db_fn, read_only = True) as inp_db:
        with Sqlite_Database(out_db_fn, read_only = False) as out_db:
            for paper_id in tqdm(paper_ids):
                paper = inp_db.get_paper_data(paper_id)
                assert paper is not None
                out_db.add_paper(paper)

    logging.info("DONE")
