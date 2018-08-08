from typing import Dict
import gzip
import json
import tqdm


def open_for_reading(filename: str):
    if filename.endswith('.gz'):
        yield from gzip.open(filename, 'rb')
    else:
        yield from open(filename, 'r')


def load_author_name_mapping(author_info_filename: str) -> Dict[str, str]:
    print(f"Loading author name mapping from {author_info_filename}")
    author_name_mapping = {}
    i = 0
    for line in tqdm.tqdm(open(author_info_filename, 'r')):
        i += 1
        try:
            author_id, name = line.split('\t')
        except ValueError:
            print(i)
            print(line)
            raise
        name = name.strip()
        if not name:
            print(f'author {author_id} has no name')
        author_name_mapping[author_id] = name
    return author_name_mapping
