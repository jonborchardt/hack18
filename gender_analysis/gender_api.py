""" Usage:
    <file-name> --in=INPUT_FILE (--key=KEY|--static=STATIC_FILE) --out=OUTPUT_FILE [--debug]
"""
# External imports
import logging
from pprint import pprint
from pprint import pformat
from docopt import docopt
import json
from urllib.request import urlopen
from urllib.parse import urlencode
from typing import Dict
from tqdm import tqdm

# Local imports

#=-----

class GenderApi:
    """
    Gender API wrapper.
    """
    def __init__(self, key: str):
        """
        Setup gender api object with an api key
        """
        self.key = key
        self.cache = {}
        self.is_limit_reached = False

    def process_name(self, name: str) -> Dict:
        """
        Get a single name response with cache and
        balance check.
        """
        if name in self.cache:
            return self.cache[name]

        if self.limit_reached():
            return False

        cur_response = self._process_name(name)
        self.cache = cur_response
        return cur_response

    def _process_name(self, name: str) -> Dict:
        """
        Get a response for a single name.
        """
        if name in self.cache:
            return self.cache[name]
        args = {"key": self.key,
                "name": name}
        args_str = urlencode(args, "utf-8")

        url = f"https://gender-api.com/get?{args_str}"
        response = urlopen(url)
        decoded = response.read().decode('utf-8')
        data = json.loads(decoded)
        self.cache[name] = data
        return data

    def limit_reached(self):
        """
        Check if limit is reached.
        """
        if self.is_limit_reached:
            # Don't ask after the first time reported exhausted
            return True
        self.is_limit_reached = self.get_stats()["is_limit_reached"]
        return self.is_limit_reached

    def get_stats(self):
        """
        Return stats for this api key.
        """
        url=f"https://gender-api.com/get-stats?&key={self.key}"
        response = urlopen(url)
        decoded = response.read().decode('utf-8')
        data = json.loads(decoded)
        return data

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    key = args["--key"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    gender_api = GenderApi(key)

    header = "First name,Count,genderize_m,genderize_f,acc,gapi_m,gapi_f"

    lines = [line.strip().split(",") for line in open(inp_fn, encoding = "utf8")][1:]
    print_flag = True

    with open(out_fn, "w", encoding = "utf8") as fout:
        fout.write(f"{header}\n")
        for cur_data in tqdm(lines):
            if len(cur_data) > 5:
                # This line already has gender_api predictions
                fout.write(",".join(cur_data) + "\n")
                continue

            if gender_api.limit_reached():
                # gender_api exhausted, just print
                if print_flag:
                    logging.info("Gender API limit reached!")
                    print_flag = False
                fout.write(",".join(cur_data) + "\n")
                continue

            name = cur_data[0]
            gender_data = gender_api.process_name(name)
            predicted_gender = gender_data["gender"]
            predicted_gender_prob = gender_data["accuracy"] / 100
            other_gender_prob = round(1 - predicted_gender_prob, 2)

            # Determine other gender
            if predicted_gender == "male":
                gapi_m = predicted_gender_prob
                gapi_f = other_gender_prob
            else:
                gapi_f = predicted_gender_prob
                gapi_m = other_gender_prob

            # Write output
            fout.write(",".join(map(str,
                                    cur_data + [gapi_m, gapi_f])) + "\n")

    credits_left = gender_api.get_stats()["remaining_requests"]
    logging.info(f"Remaining requests = {credits_left}")
    logging.info("DONE")
