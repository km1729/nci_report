import sqlite3
import json
import yaml
import util
import sql
# db name
db_file = './sql/ncireport.db'

# establish a connection
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

config = util.read_config()

config_data = util.read_config()
# get list of gdata, scratch, compute
gdata = config_data['gdata']
scratch = config_data['scratch']
compute = config_data['compute']


query_result = sql.query("lquota",fs='gdata')
lquota_dataset = {}
for result in query_result:
    id, project, datetime, type, usage,quota,dLimit, iusage, iQuota, iLimit = result
    
    if project not in lquota_dataset:
        lquota_dataset[project]= {"type":type, \
                              "date": [],
                              "usage": [],
                              "quota": [],
                              "limit": [],
                              "iusage":[],
                              "iQuota": [],
                              "iLimit":[]}
    lquota_dataset[project]["date"].append(datetime)
    lquota_dataset[project]["usage"].append(usage)
    lquota_dataset[project]["quota"].append(quota)
    lquota_dataset[project]["limit"].append(dLimit)
    lquota_dataset[project]["iusage"].append(iusage)
    lquota_dataset[project]["iQuota"].append(iQuota)
    lquota_dataset[project]["iLimit"].append(iLimit)
    
with open('output.json', 'w') as json_file:
    json.dump(lquota_dataset, json_file, indent=2)   

    