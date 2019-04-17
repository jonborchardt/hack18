from typing import Dict
import gzip
import json
import tqdm
import pdb


def get_gender_prob(gender_dict: Dict, author: Dict) -> Dict:
    """
    Get the gender of a given author according to a
    gender dict.
    """
    first_name = author["first_name"].lower()
    if first_name in gender_dict:
        return gender_dict[first_name]
    else:
        # Default to unknown
        return {"male": 0.5,
                "female": 0.5}

def load_name_probs(filename: str) -> Dict[str, Dict[str, float]]:
    """
    Return a dictionary from name to probability of (male, female).
    """
    lines = []
    # for line in open(filename, encoding = "cp1251"):
    #     print(line.strip())
    lines = [line.strip().split(",") for line in tqdm.tqdm(open(filename, encoding = "utf8"))]
    names_dict = {}
    for line in lines[1:]:
        name = line[0]
        cur_dict = {}
        if (len(line) == 5):
            cur_dict["male"] = float(line[2])
            cur_dict["female"] = float(line[3])
        else:
            cur_dict["male"] = float(line[5])
            cur_dict["female"] = float(line[6])
        names_dict[name] = cur_dict

    return names_dict


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


if __name__ == "__main__":
    x = load_name_probs("merged_names_dblp.csv")
