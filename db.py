import os
import sqlite3
from sqlite3 import Error
from fetch import get_tags


def create_db_con(path):
    """Returns a sqlite3 connection object"""
    try:
        return sqlite3.connect(path)
    except Error as e:
        print(e)


def clear_db(path):
    """Removes existing database file"""
    if os.path.exists(path):
        os.remove(path)


def update_db(path, data_hash):
    """Create and fill a sqlite3 database"""
    con = create_db_con(path)
    con.execute('''CREATE VIRTUAL TABLE entries
             USING FTS5(title, url, tags, note)''')
    sql = '''INSERT INTO entries(title, url, tags, note) VALUES(?,?,?,?)'''
    cur = con.cursor()
    for _, v in data_hash.items():
        vals = (v[0], v[1], get_tags(v), v[3])
        cur.execute(sql, vals)
    con.commit()
