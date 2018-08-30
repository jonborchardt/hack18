#!/bin/bash
# Usage:
#      run_analyses.sh <input-file> <output-folder>
# Run all analyses on full data with gender
set -e

echo "concat..."
cat ../../open-corpus/medline-clean-gender/s2-corpus-* > ../../open-corpus/medline-clean-gender.jsonl

mkdir -p ${2}/common_names

echo "cmmon names..."
python count_names_by_gender.py  --in=$1  --out=$2/common_names/

echo "gender by year..."
python gender_count_by_year.py --in=$1  --out=$2/gender_by_year.csv

echo "in citations by year..."
python in_citations_by_gender.py --in=$1 --out=$2/in_citation_by_year.csv

echo "collab..."
python analyze_collab.py  --in=$1 --out=$2/collab.csv

echo "DONE"
