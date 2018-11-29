#!/bin/bash
# Usage:
#      run_analyses.sh <input-file> <output-folder>
# Run all analyses on full data with gender
set -e

#0. Paper count
echo "Counting papers"
python paper_count_by_year.py --in=$1 --out=$2/paper_cnt.csv

#1. Authorship
echo "Authorship"
python gender_count_by_year.py --in=$1  --out=$2/gender_by_year.csv

#2. Collaboration
echo "collab..."
python analyze_collab.py  --in=$1 --out=$2/collab.csv

#3. Citation
# Generate SQL
echo "generate sql..."
python add_gender_to_db.py --in=$1  --out=./${1}.sqlite

# Analyze with SQL
echo "citations"
python analyses_with_db.py --db=${1}.sqlite  --json=${1}  --out=${2}

# Rarely used:
# mkdir -p ${2}/common_names
# echo "common names..."
# python count_names_by_gender.py  --in=$1  --out=$2/common_names/


echo "DONE"


# Deprecated:

# echo "in citations by year..."
# python in_citations_by_gender.py --in=$1 --out=$2/in_citation_by_year.csv

# echo "out citations by year..."
# python out_citations_by_gender.py --in=$1 --out=$2/out_citation_by_year.csv
