'''
This script offers handy functions for 
managing settings, running shell commands, making backups, and logging events. 
It's configurable via the config.yml file and carries out file operations 
based on the provided settings
'''

import yaml
import subprocess
import os
import logging

config_file='/g/data/dp9/km0642/learning/nci_report/config.yml'

def read_config():
    with open(config_file, 'r') as file:    
        return yaml.safe_load(file) 

def exist_folder(path):
    # Ensure the specified directory exists; create if not
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def account_cmd(command, filename):
    config_data = read_config()
    tmp_file_path = os.path.join(exist_folder(config_data['default']['temp_file_path']), filename)

    completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    if completed_process.returncode == 0:        
        with open(tmp_file_path, 'w') as file:
            file.write(completed_process.stdout)
    else:
        print("Error executing the command")

def create_backup(filename, date):
    try: 
        config_data = read_config()
        archive_path = exist_folder(config_data['default']['archive'])
        archive_file_path = os.path.join(archive_path, filename)

        read_file_path = os.path.join(config_data['default']['temp_file_path'], filename)

        with open(read_file_path, 'r') as read_file, open(archive_file_path, 'a') as write_file:
            write_file.write(f"{date}\n{read_file.read()}")

        os.remove(read_file_path)
        log(filename)

        message = f"Archive completed for {filename} on {date}"
        logging.info(message) 
        print(message)

    except Exception as e:
        logging.error(f"Error during archiving: {str(e)}")
        print(f"Error during archiving: {str(e)}")

def log(filename):
    config_data = read_config()
    tmp_file_path = exist_folder(config_data['default']['temp_file_path'])
    log_filename = os.path.join(tmp_file_path, f"{filename}.log")

    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
