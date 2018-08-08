from typing import Dict
import gzip
import json
import os
import sys
import tqdm

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
from gender_analysis.util import open_for_reading, load_author_name_mapping


def main(original_data_directory: str,
         cleaned_data_directory: str,
         author_info_filename: str = 'author_data.tsv'):
    if not original_data_directory.endswith('/'):
        original_data_directory += '/'
    if not cleaned_data_directory.endswith('/'):
        cleaned_data_directory += '/'
    os.makedirs(cleaned_data_directory, exist_ok=True)
    author_name_mapping = load_author_name_mapping(author_info_filename)
    for root, _, files in os.walk(original_data_directory):
        new_root = root.replace(original_data_directory, cleaned_data_directory)
        for filename in files:
            clean_file(root + filename,
                       new_root + filename.replace('.gz', '.jsonl'),
                       author_name_mapping)


def clean_file(in_file: str,
               out_file: str,
               author_name_mapping: Dict[str, str]):
    print(f"Reading file at {in_file}, outputting cleaned file to {out_file}")
    out = open(out_file, 'w')
    total_records = 0
    num_invalid = 0
    for line in tqdm.tqdm(open_for_reading(in_file)):
        total_records += 1
        json_blob = json.loads(line)
        record = {}
        try:
            authors = []
            for author in json_blob['authors']:
                if author['ids']:
                    author_id = author['ids'][0]
                    author_name = author_name_mapping[author_id]
                else:
                    author_name = author['name']
                authors.append(author_name)
            record['authors'] = authors
            record['year'] = json_blob['year']
            record['venue'] = json_blob['venue']
            record['id'] = json_blob['id']
            record['inCitations'] = json_blob['inCitations']
            record['outCitations'] = json_blob['outCitations']
        except KeyError:
            num_invalid += 1
            continue
        json.dump(record, out)
        out.write('\n')
    out.close()
    print(f"{num_invalid} records invalid out of {total_records}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
