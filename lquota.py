import os
import json
from datetime import datetime
import subprocess

command = "lquota --no-pretty-print"

completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
if completed_process.returncode == 0:
    with open("lquota.txt", "a") as file:
        file.write(completed_process.stdout)
else:
    print("Error executing the command")

# Directory to store the log files
log_directory = 'log'

# Check if the log directory exists, if not, create it
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Reading the file
file_path = 'lquota.txt' 
with open(file_path, 'r') as file:
    data = file.readlines()

# Processing the lquota data
keys = ["prj", "fs", "Usage", "Quota", "Limit", "iUsage", "iQuota", "iLimit"]

# Create timestamp
nowday = datetime.today().strftime("%Y%m%d%H%M%S")
lquota = {}
for line in data[2:]:  # Skip the first two lines of the file as they contain the headers and separator
    values = line.split()

    if len(values) == len(keys):
        station = values[0]
        data = {
            "fs": values[1],
            "project": values[0],
            "timestamp": nowday,
            "Usage": values[2],
            "Quota": values[3],
            "Limit": values[4],
            "iUsage": values[5],
            "iQuota": values[6],
            "iLimit": values[7]
        }

        # Construct the file path
        file_path = os.path.join(log_directory, f"lquota.json")


        # Write the updated content back to the file
        with open(file_path, 'a') as file:
            json.dump(data, file, indent=4)
