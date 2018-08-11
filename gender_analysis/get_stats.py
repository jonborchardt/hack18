#!/usr/bin/env python

import argparse, json, os, re
from os import path
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
le_gender = leGenderary(options)

def get_gender_stats(id2paper):
    stats = []
    for i, (_id, paper) in enumerate(id2paper.items()):
        if i % 25000 == 0: print i
        if len(paper['authors']) == 0: continue

        in_authors, out_authors = list(), list()
        for _in in paper['inCitations']:
            if _in in id2paper:
                in_authors.extend(id2paper[_in]['authors'])
        for _out in paper['outCitations']:
            if _out in id2paper:
                out_authors.extend(id2paper[_out]['authors'])

        in_genders = [auth['gender'] for auth in in_authors]
        out_genders = [auth['gender'] for auth in out_authors]

        in_fem, in_male, in_unknown = \
                    in_genders.count('female'), in_genders.count('male'), in_genders.count('unknown')
        out_fem, out_male, out_unknown = \
                    out_genders.count('female'), out_genders.count('male'), out_genders.count('unknown')

        stats.append({'authors' : paper['authors'],
                      'venue': paper['venue'],
                      'year' : paper['year'],
                      'inCitationsCount' : {'female' : in_fem,
                                            'male' : in_male,
                                            'unknown' : in_unknown},
                      'outCitationsCount' : {'female' : out_fem,
                                             'male' : out_male,
                                             'unknown' : out_unknown}})
    return stats
    

def determine_first_name(full_name):
    #print 'full', full_name
    first_name = le_gender.determineFirstName(full_name.split(' '))
    # edge cases not covered by leGenderary
    if first_name == '':
        if re.match('[a-z]\.*', full_name.lower()):
            first_name = full_name[0]
        elif len(full_name.split(' ')[0]) == 2 and full_name.split(' ')[0][1] == '.':
            # non-ascii first letterletter
            first_name = full_name[0]
        else: # non-ascii first name
            first_name = full_name.split(' ')[0]
    return first_name.lower()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('--subset', dest='subset_fname', type=str, required=True,
                        help='path to subset of S2 papers')
    parser.add_argument('--out', type=str, default='../data/citation_rates.json')
    args = parser.parse_args()
    
    # load gender data and papers
    with open(args.subset_fname, 'r') as f:
        id2paper = {x['id']:x for x in [json.loads(l.strip('\n')) for l in f.readlines()]}
        stats = get_gender_stats(id2paper)
        with open(args.out, 'w') as f:
            [f.write('{}\n'.format(json.dumps(st))) for st in stats]
