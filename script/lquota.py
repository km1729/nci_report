'''
The code imports functions from `sql.py` and `util.py` 
to capture and process lquota output, saving it to a text file. 
The script then ingests this data into an SQLite database. 
After processing, the saved file is updated as a backup and subsequently deleted.
'''

from datetime import datetime

import sql
import util

process_file = 'lquota.txt'

config_data = util.read_config()
tmp_file = config_data['default']['temp_file_path']
file_path = f"{tmp_file}/{process_file}"

# run lquota command and save the output
util.account_cmd("lquota --no-pretty-print", process_file)

with open( file_path, 'r') as file:
    lquota_data = file.readlines()
    
# columns in the lquota data
# keys = ["prj", "fs", "Usage", "Quota", "Limit", "iUsage", "iQuota", "iLimit"]

# Create timestamp
nowday = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
for line in lquota_data[2:]: 
    values = line.split()

    if len(values) == 8:

        project_id = sql.get_project_id(values[0])
        if values[1] == 'gdata':
            fs = 1
        elif values[1] == 'scratch':
            fs = 2
        usage= float(values[2])
        quota= float(values[3])
        dLimit= float(values[4])
        iUsage= float(values[5])
        iQuota= float(values[6])
        iLimit= float(values[7])

        data = ( project_id[0], nowday, fs, usage, quota, dLimit,iUsage,iQuota, iLimit)
        
        sql.ingest_lquota(data)

util.create_backup(process_file, nowday)
