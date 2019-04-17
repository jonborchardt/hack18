#!/bin/bash
# Usage:
#      run_analyses.sh <input-file> <gender-fn> <output-folder>
# Run all analyses on full data with gender
set -e

#0. Paper count
# echo "Counting papers"
# python paper_count_by_year.py --in=$1 --out=$3/paper_cnt.csv

# #1. Authorship
echo "Authorship"
python gender_count_by_year.py --in=$1 --gender=$2  --out=$3/authorship.csv

# # #2. Collaboration
echo "collab..."
python analyze_collab.py  --in=$1 --gender=$2 --out=$3/collab.csv

# #3. Citation
# # Generate SQL
# echo "generate sql..."
# python add_gender_to_db.py --in=$1  --out=${1}.sqlite

# Analyze with SQL
# echo "citations"
# python analyses_with_db.py --json=${1} --db=${1}.sqlite --gender=$2 --out=${3}

# Rarely used:
# mkdir -p ${2}/common_names
# echo "common names..."
# python count_names_by_gender.py  --in=$1  --out=$3/common_names/ &


echo "DONE"


