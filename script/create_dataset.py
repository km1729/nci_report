import sqlite3
import json
import util
import database as db
# import os

# db name
config_data = util.read_config()
db_file = config_data['default']['db_file']

# establish a connection
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# get list of gdata compute projects
gdata_projects = config_data['gdata']
scratch_projects = config_data['scratch']

def process_project_data(project_type, projects):
    for project in projects:
        query_condition = f"type='{project_type}' AND project='{project}'"
        query_result = db.query("lquota_view", condition=query_condition)

        lquota_dataset = {
            "disk": [],
            "inode": []
        }

        project_lquota = {
            "datetime": [],
            "disk": {
                "Usage": [],
                "Quota": [],
                "Limit": []
            },
            "inode": {
                "IUsage": [],
                "IQuota": [],
                "ILimit": []
            }
        }

        # query the lquota data and create a list
        for result in query_result:
            id, project, datetime, type, usage, quota, dLimit, iusage, iQuota, iLimit = result

            project_lquota['datetime'].append(datetime)
            project_lquota['disk']['Usage'].append(usage)
            project_lquota['disk']['Quota'].append(quota)
            project_lquota['disk']['Limit'].append(dLimit)
            project_lquota['inode']['IUsage'].append(iusage)
            project_lquota['inode']['IQuota'].append(iQuota)
            project_lquota['inode']['ILimit'].append(iLimit)

        # create Json data structure        
        lquota_dataset["disk"].append({
            "prj": project,
            "name": f"{type} disk Usage",
            "x": project_lquota['datetime'],
            "y": project_lquota['disk']['Usage'],
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"color": "blue"}
        })
        # lquota_dataset["disk"].append({
        #     "prj": project,
        #     "name": f"{type} disk Quota",
        #     "x": project_lquota['datetime'],
        #     "y": project_lquota['disk']['Quota'],
        #     "type": "scatter",
        #     "mode": "lines",
        #     "line": {"color": "orange"}
        # })
        lquota_dataset["disk"].append({
            "prj": project,
            "name": f"{type} disk Limit",
            "x": project_lquota['datetime'],
            "y": project_lquota['disk']['Limit'],
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"color": "red"}
        })

        # Add other disk entries (Quota, Limit) similarly

        lquota_dataset["inode"].append({
            "prj": project,
            "name": f"{type} inode usage",
            "x": project_lquota['datetime'],
            "y": project_lquota['inode']['IUsage'],
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"color": "blue"}
        })
        # lquota_dataset["inode"].append({
        #     "prj": project,
        #     "name": f"{type} inode IQuota",
        #     "x": project_lquota['datetime'],
        #     "y": project_lquota['inode']['IQuota'],
        #     "type": "scatter",
        #     "mode": "lines",
        #     "line": {"color": "orange"}
        # })
        lquota_dataset["inode"].append({
            "prj": project,
            "name": f"{type} inode ILimit",
            "x": project_lquota['datetime'],
            "y": project_lquota['inode']['ILimit'],
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"color": "red"}
        })

        # Add other inode entries (IQuota, ILimit) similarly
        data_storage = config_data['default']['data_stroage']

        with open(f'{data_storage}/{project}_{project_type}_lquota_output.json', 'w') as json_file:
            json.dump(lquota_dataset, json_file, indent=2)

# Process gdata projects
process_project_data('gdata', gdata_projects)

# Process scratch projects
process_project_data('scratch', scratch_projects)