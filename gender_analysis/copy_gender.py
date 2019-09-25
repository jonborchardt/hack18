""" Usage:
    <file-name> --in=INPUT_FILE --annot=ANNOTATED_FILE --out=OUTPUT_FILE [--debug]
"""
# External imports
import logging
from pprint import pprint
from pprint import pformat
from docopt import docopt
import pdb
# Local imports

#=-----

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    annot_fn = args["--annot"]
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    lines_to_annot = [line.strip().split(",") for line in open(inp_fn, encoding = "utf8")][1:]
    ref_lines = [line.strip().split(",") for line in open(annot_fn, encoding = "utf8")][1:]

    ref_dict = {}
    for ls in ref_lines:
        if len(ls) == 7:
            name = ls[0]
            ref_dict[name] = ls[-2 : ]

    total_acc = 0
    prev_acc = 0
    with open(out_fn, "w", encoding = "utf8") as fout:
        fout.write("First name,Count,genderize_m,genderize_f,acc,gapi_m,gapi_f\n")
        for cur_line in lines_to_annot:
            name = cur_line[0]
            to_write = cur_line
            cur_acc = float(cur_line[-1])
            if name in ref_dict:
                total_acc += cur_acc - prev_acc
                to_write += ref_dict[name]
            prev_acc = cur_acc
            to_write_str = ",".join(to_write)
            fout.write(f"{to_write_str}\n")

    logging.info(f"Found match for {total_acc} of the data")


    logging.info("DONE")
