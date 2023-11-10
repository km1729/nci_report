'''
provides two functions for interacting with the SQLite database: 
one for querying and potentially adding records to the project table, and 
another for inserting records into the lquota table
'''
import sqlite3

# db name
db_file = './sql/ncireport.db'

# establish a connection
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# check if the project is exist
def get_project_id(prj):
    '''
    Get project id from the project table.
    If it doesn't exist, add the project name.
    Return a tuple with the project id.
    '''
    cursor.execute(f'SELECT id FROM project WHERE prj_name = ? ', (prj,))
    result = cursor.fetchone()
    
    if result == None:
        cursor.execute('INSERT INTO project (prj_name) VALUES (?)', (prj,))
        conn.commit()  
        cursor.execute('SELECT id FROM project WHERE prj_name = ?', (prj,))
        result = cursor.fetchone()
    return result

def ingest_lquota(data):
    '''
    Ingest data into the lquota table.
    '''
    cursor.execute('INSERT INTO lquota VALUES (NULL,?,?,?,?,?,?,?,?,?)', data)
    conn.commit() 

def query(db_table, project=None, fs=None):
    db_table = f"{db_table}_view"
    if project is None and fs is None:
        # Execute select * from db_table when both project and fs are None
        cursor.execute(f'SELECT * FROM {db_table}')
    elif project is not None and fs is None:
        # Execute select * from db_table where project=project when project is specified and fs is None
        cursor.execute(f'SELECT * FROM {db_table} WHERE project = ?', (project,))
    elif project is None and fs is not None:
        # Execute select * from db_table where fs=fs when fs is specified and project is None
        cursor.execute(f'SELECT * FROM {db_table} WHERE type = ?', (fs,))
    else:
        # Execute select * from db_table where project=project and fs=fs when both project and fs are specified
        cursor.execute(f'SELECT * FROM {db_table} WHERE project = ? AND type = ?', (project, fs))
    
    result = cursor.fetchall()
    conn.commit()
    return result

