#!/bin/bash
# Usage:
#      run_analyses.sh
# Run all analyses on full data with gender
set -e

echo "gender by year..."
python gender_count_by_year.py --in=../data/dblp_partial.gender.jsonl  --out=../data/gender_by_year_dblp_partial.csv

echo "in citations by year..."
python in_citations_by_gender.py --in=../data/dblp_partial.gender.jsonl --out=../data/in_citation_by_year.csv

echo "cmmon names..."
python count_names_by_gender.py  --in=../data/dblp_partial.gender.jsonl      --out=../data/common_names/

echo "DONE"
