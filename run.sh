#!/bin/bash


# # Execute lquota.py to fetch lquota and store it in an SQLite database
source /g/data/hh5/public/apps/miniconda3/etc/profile.d/conda.sh
conda activate stats
python3 script/lquota.py


# Run create_dataset.py to generate JSON files from queried data
source /g/data/hh5/public/apps/miniconda3/etc/profile.d/conda.sh
conda activate stats
python3 script/create_dataset.py

# if [ $? -ne 0 ]; then
#     echo "Error occurred." 
# fi
