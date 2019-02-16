# -*- coding: utf-8 -*-
"""

Read implements function to read and output data
from the sqlite3 database containing all pocket items

"""
import sys
import json
from pprint import pprint
import texttable
from db import create_db_con


def get_cur(path):
    """Returns a cursor to the sqlite3 db
    Args:
        path (str): path to sqlite3 db
    Returns:
        cur (cursor)
    """
    con = create_db_con(path)
    cur = con.cursor()
    return cur


def select_col(path, col):
    """Returns a given col
    Args:
        path (str): path to sqlite3 db
        col (int): column of database
            0 = titles
            1 = urls
            2 = tags
            3 = created
            4 = note
    Returns:
        dict with results from query
    """
    con = create_db_con(path)
    con.row_factory = lambda cursor, row: row[col]
    sql = '''SELECT * FROM entries'''
    cur = con.cursor()
    return cur.execute(sql).fetchall()


def get_tags_stats(col, sort):
    """List statistics about tags of entries
    Args:
        col (str): column of table
        sort (bool): if output should be sorted
    """
    tags = {}
    for row in col:
        for tag in row.split():
            tags[tag] = tags.get(tag, 0) + 1
    if sort:
        sorted_by_value = sorted(tags.items(), key=lambda kv: kv[1])
        pprint(sorted_by_value)
    else:
        print(json.dumps(tags))


def list_entries(path, col, terms):
    """Filters and lists entries
    Args:
        path (str): path to sqlite3 database
        col (str): column of table
        term (list): list of terms to be filtered
    Returns:
        entries (dict) matching the patterns
    """
    cur = get_cur(path)
    sql = ""
    if col == 'complete':
        if terms:
            terms = ' AND '.join(terms)
            sql = 'SELECT * FROM entries WHERE entries MATCH ?'
            entries = cur.execute(sql, (terms,)).fetchall()
        else:
            sql = 'SELECT * FROM entries'
            entries = cur.execute(sql).fetchall()
    else:
        if terms:
            terms = ' AND '.join(terms)
            sql = 'SELECT * FROM entries WHERE {} MATCH ?'.format(col)
            entries = cur.execute(sql, (terms,)).fetchall()
        else:
            print("Warning: col without search term not useful")
            sys.exit(1)
    return entries


def view_entries(entries, width, count, parsable):
    """Print a filtered set of entries
    Args:
        entries (dict): entries to be viewed
        width (int): width of the column
        count (bool): prints total amount of entries
        parsable: (bool): prints the result in a parsable format
    """
    if parsable:
        print(entries)
    else:
        table = texttable.Texttable()
        table.set_cols_width([width, width, 15, 10, 15])
        for row in entries:
            print(row)
            table.add_row(list(row))
        print(table.draw() + "\n")
    if count:
        print("Found entries: {} \n".format(len(entries)))
