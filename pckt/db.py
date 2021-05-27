# -*- coding: utf-8 -*-
"""

db implements functionality to create a local sqlite3 database
containing Pocket items from the fetch module

"""
import os
import sqlite3
from sqlite3 import Error
from fetch import get_tags


def create_db_con(path):
    """Returns a sqlite3 connection object
    Args:
        path (str): path to database
    Returns:
        sqlite3 connection object
    """
    try:
        return sqlite3.connect(path)
    except Error as e:
        print(e)


def clear_db(path):
    """Removes existing database file
    Args:
        path (str): path to database
    """
    if os.path.exists(path):
        os.remove(path)


def update_db(path, data):
    """Create and fill a sqlite3 database
    Args:
        path (str): path to database
        data (dict): inserts data dictionary into db
    """
    con = create_db_con(path)
    con.execute('''CREATE VIRTUAL TABLE entries
             USING FTS5(title, url, tags, created, note)''')
    sql = '''INSERT INTO entries(title, url, tags, created, note) VALUES(?,?,?,?,?)'''
    cur = con.cursor()
    for _, v in data.items():
        vals = (v[0], v[1], get_tags(v), v[3], v[4])
        cur.execute(sql, vals)
    con.commit()
    con.close()
