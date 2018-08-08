from collections import defaultdict
from typing import Dict, Set
import json
import os
import sys
import tqdm

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
from gender_analysis.util import open_for_reading


def main(data_path: str, output_author_filename: str):
    author_info: Dict[str, Set[str]] = defaultdict(set)
    if os.path.isdir(data_path):
        i = 0
        for root, _, files in os.walk(data_path):
            for filename in files:
                i += 1
                get_authors_from_file(root + filename, author_info)
                print("Finished scanning {i} records")
                print(f"Found {len(author_info)} unique author ids so far")
    else:
        get_authors_from_file(data_path, author_info)

    print(f"Found {len(author_info)} unique author ids")
    output_author_info(author_info, output_author_filename)


def get_authors_from_file(data_filename: str, author_info: Dict[str, Set[str]]):
    print(f"Reading author info from {data_filename}")
    for line in tqdm.tqdm(open_for_reading(data_filename)):
        json_blob = json.loads(line)
        for author in json_blob['authors']:
            if len(author['ids']) > 1:
                print(f"Found author with multiple IDs... {author}")
            for author_id in author['ids']:
                author_info[author_id].add(author['name'])


def output_author_info(author_info: Dict[str, Set[str]], filename: str):
    print(f"Getting longest name for each auther")
    longest_names = {}
    for author_id, author_names in author_info.items():
        longest_name = sorted(author_names, key=lambda x: -len(x))[0]
        longest_name = longest_name.replace('\n', '')
        longest_name = longest_name.replace('\t', '')
        longest_names[author_id] = longest_name
    print(f"Saving author info to {filename}")
    with open(filename, 'w') as out:
        for author_id, author_name in longest_names.items():
        out.write(f"{author_id}\t{author_name}\n")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
