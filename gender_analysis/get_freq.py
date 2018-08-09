#!/usr/bin/env python

import argparse, json, os, re
from os import path
from collections import Counter
from legenderary.leGenderary import leGenderary

options = { 'male'          : 'male',
            'female'        : 'female',
            'androgynous'   : 'androgynous',
            'unknown'       : 'unknown',
            'maleConfirm'   : 'male needs confirmation',
            'femaleConfirm' : 'female needs confirmation',
            'dict1'         : 'legenderary/dict1.txt',
            'dict2'         : 'legenderary/dict2.txt',
            'customDict'    : 'legenderary/custom.txt',
            'bingAPIKey'    : 'ABC123478ZML'
          }
gender = leGenderary(options)

def parse_args():
    parser = argparse.ArgumentParser('Get top-k most frequent first author names')
    parser.add_argument('--k', type=int, default=100)
    parser.add_argument('--s2', type=str, default='../data/cleaned', help='path to s2 files')
    parser.add_argument('--out', type=str, default='../data/top_k.csv')
    return parser.parse_args()

def load_s2_data(s2_path):
    fpaths = filter(lambda fp: re.match('s2-corpus-[0-9]+', fp), os.listdir(s2_path)) # s2 corpus files
    num_missing=0
    first_authors = []
    for fp in sorted(fpaths):
        with open(path.join(s2_path, fp), 'r') as f:
            lines = []
            for i, line in enumerate(f):
                if i% 100000 ==0: print 'on item {} for {}'.format(i, fp)
                as_json = json.loads(line)
                if len(as_json['authors']) == 0:
                    num_missing+=1
                    continue

                full_name = as_json['authors'][0]#['name']
                first_authors.append(get_first_name(full_name))
    print '{} missing author'.format(num_missing)
    return first_authors

def get_first_name(full_name):
    first_name = gender.determineFirstName(full_name.split(' '))

    if first_name == '':     # edge cases not covered by leGenderary
        if re.match('[a-z]\.*', full_name.lower()):
            first_name = full_name[0]
        elif len(full_name.split(' ')[0]) == 2 and full_name.split(' ')[0][1] == '.': # non-ascii first letterletter
            first_name = full_name[0]
        else: # non-ascii first name
            first_name = full_name.split(' ')[0]
    return first_name.lower()
    
if __name__ == '__main__':
    args = parse_args()

    first_names = load_s2_data(args.s2)
    no_single_letters = filter(lambda x: len(x) > 1, first_names)
    
    freq_counts = sorted(Counter(no_single_letters).items(),
                         key=lambda x: x[1],
                         reverse=True)
    top_k = freq_counts[0:args.k]

    with open(args.out, 'w') as f:
        f.write('Name,Count,Gabi,Candace,Jonathan,Matt\n')
        [f.write('{},{}\n'.format(name.encode('utf8'), count)) for name, count in freq_counts[0:args.k]]
        
    
