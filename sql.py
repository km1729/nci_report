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
