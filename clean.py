"""
Simple python script to double check database and make sure every row has a
year, make and model
"""

import sqlite3
import os
import sys

def get_bad_rowids(dbconn, table_name):
    cursor = dbconn.cursor()
    badies = []
    query_all = "SELECT rowid, * FROM {}".format(table_name)
    for row in cursor.execute(query_all):
        if row[1] == None \
        or row[2] == None \
        or row[3] == None:
            # If year, make, or model are None, add rowid to badiess
            badies.append(row[0])
    return badies


def clean(dbconn, table_name, badies):
    cursor = dbconn.cursor()
    for rowid in badies:
        sql_delete = "DELETE FROM {} WHERE rowid={}".format(table_name, rowid)
        cursor.execute(sql)
    dbconn.commit()


    

if __name__ == "__main__":
    path = './Motorcycles.sqlite'
    table_name = 'Motorcycles'
    if not os.path.isfile(path):
        raise Exception("No sqlite database file at this path")
    dbconn = sqlite3.connect(path)
    get_bad_rowids(dbconn, table_name)


    