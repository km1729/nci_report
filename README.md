

lquota.py  
The code imports functions from `sql.py` and `util.py` to capture and process lquota output, saving it to a text file. The script then ingests this data into an SQLite database. After processing, the saved file is updated as a backup and subsequently deleted.


sql.py  
provides two functions for interacting with the SQLite database: 
- querying and potentially adding records to the project table
- inserting records into the lquota table

util.py  
This script offers handy functions for managing settings, running shell commands, making backups, and logging events. 
It's configurable via the config.yml file and carries out file operations based on the provided settings




module use /g/data3/hh5/public/modules
module load conda
conda activate